from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Iterable, List, Tuple

from prefect import flow, task
import mlflow

from .config import PipelineConfig, StageConfig

from .base import BaseModule


class Orchestrator:
    """Pipeline orchestrator that loads and runs configured modules."""

    def __init__(self, cfg: Iterable[StageConfig]):
        self.stages: List[Tuple[BaseModule, bool]] = []
        for stage_conf in cfg:
            module_path = stage_conf.module
            module_name, class_name = module_path.rsplit(".", 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            if not issubclass(cls, BaseModule):
                raise TypeError(f"{module_path} is not a BaseModule")
            stage_instance = cls(stage_conf.config)
            self.stages.append((stage_instance, stage_conf.enable_mlflow))

    def _build_tasks(self) -> list:
        tasks = []
        for stage, use_mlflow in self.stages:
            @task(name=stage.__class__.__name__)
            def stage_task(data, _stage=stage, _ml=use_mlflow):
                if _ml:
                    with mlflow.start_run(nested=True):
                        return _stage.run(data)
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

        return pipeline()