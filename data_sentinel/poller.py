import os
import time
from kubernetes import client, config as kube_config

from data_sentinel.config.config import PipelineConfig
from kafka import KafkaConsumer, TopicPartition
import socket

TOPIC = "RTI"
NAMESPACE = "default"
DEPLOYMENT = "worker-deployment"
KAFKA_BOOTSTRAP = "192.168.0.12:9092"

def scale(n):
    apps = client.AppsV1Api()
    apps.patch_namespaced_deployment_scale(
        name=DEPLOYMENT,
        namespace=NAMESPACE,
        body={"spec": {"replicas": n}}
    )
    print(f"Scaled to {n} replicas")

class Poller:
    def __init__(self, cfg: PipelineConfig):
        try:
            socket.create_connection(("192.168.0.12", 9092), timeout=5)
            print("[Scaler] Kafka is reachable", flush=True)
        except Exception as e:
            print(f"[Scaler] Cannot connect to Kafka: {e}", flush=True)
        self.path = cfg.poll.polling_path
        self.max_workers = cfg.poll.max_workers
        self.consumer = KafkaConsumer(
            bootstrap_servers="192.168.0.12:9092",
            group_id="controller-group",
            enable_auto_commit=False
        )
        # Wait for partitions to be available
        retries = 5
        while retries:
            partitions = self.consumer.partitions_for_topic(TOPIC)
            print(f"[Scaler] Partitions for topic {TOPIC}: {partitions}", flush=True)
            if partitions:
                break
            print("[Scaler] Waiting for Kafka metadata...")
            time.sleep(1)
            retries -= 1

        if not partitions:
            raise RuntimeError(f"[Scaler] Failed to fetch partitions for topic: {TOPIC}")

        self.topic_partitions = [TopicPartition(TOPIC, p) for p in partitions]
        self.consumer.assign(self.topic_partitions)

        kube_config.load_incluster_config()
        self.apps = client.AppsV1Api()
        print(f"[Scaler] Initialized with path: {self.path}, max workers: {self.max_workers}")

    def get_total_lag(self):
        total_lag = 0
        print(f"[Scaler] Partitions: {self.topic_partitions}", flush=True)
        end_offsets = self.consumer.end_offsets(self.topic_partitions)
        for tp in self.topic_partitions:
            try:
                latest = end_offsets[tp]
                committed = self.consumer.committed(tp)
                if committed is None:
                    committed = 0  # If no committed offset, assume 0
                lag = latest - committed
                print(f"[Scaler] Partition {tp.partition} lag: {lag}", flush=True)
                total_lag += lag
            except Exception as e:
                print(f"[Scaler] Error in lag calc for {tp}: {e}", flush=True)
        print(f"[Scaler] Total lag across all partitions: {total_lag}", flush=True)
        return total_lag

    def scale(self, lag):
        if lag == 0:
            print("[Scaler] No lag detected, no scaling needed.")
            return
        replicas = min(self.max_workers, lag // 10 + 1)
        self.apps.patch_namespaced_deployment_scale(
            name=DEPLOYMENT,
            namespace=NAMESPACE,
            body={"spec": {"replicas": replicas}}
        )
        print(f"[Scaler] Lag: {lag}, Scaled to: {replicas} pods")

    def run(self):
        while True:
            try:
                print("[Scaler] Checking lag...", flush=True)
                lag = self.get_total_lag()
                self.scale(lag)
            except Exception as e:
                print(f"[Scaler] ERROR: {e}")
            time.sleep(10)
