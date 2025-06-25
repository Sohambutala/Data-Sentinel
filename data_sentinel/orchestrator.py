from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Iterable, List

from .base import BaseModule


class Orchestrator:
    """Pipeline orchestrator that loads and runs configured modules."""

    def __init__(self, stages: Iterable[dict]):
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

    def run(self) -> Any:
        data: Any = None
        for stage in self.stages:
            data = stage.run(data)
        return data


def load_config(path: str | Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    return cfg.get("pipeline", [])
