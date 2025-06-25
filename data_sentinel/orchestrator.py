from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Iterable, List

from prefect import flow, task
import mlflow

from .base import BaseModule


class Orchestrator:
    """Pipeline orchestrator that loads and runs configured modules."""

    def __init__(self, stages: Iterable[dict], use_mlflow: bool = False):
        self.use_mlflow = use_mlflow
        self.stages: List[BaseModule] = []
        for stage_conf in stages:
            module_path = stage_conf["module"]
            config = stage_conf.get("config", {})
            module_name, class_name = module_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            if not issubclass(cls, BaseModule):
                raise TypeError(f"{module_path} is not a BaseModule")
            self.stages.append(cls(config))

    def _build_tasks(self) -> list:
        tasks = []
        for stage in self.stages:
            @task(name=stage.__class__.__name__)
            def stage_task(data, _stage=stage):
                return _stage.run(data)

            tasks.append(stage_task)
        return tasks

    def run(self) -> Any:
        tasks = self._build_tasks()

        @flow(name="data_sentinel_pipeline")
        def pipeline() -> Any:
            data: Any = None
            for t in tasks:
                data = t(data)
            return data

        if self.use_mlflow:
            with mlflow.start_run():
                return pipeline()
        return pipeline()


def load_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    return cfg
