from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Any, Dict, List


class StageConfig(BaseModel):
    """Configuration for a single pipeline stage."""

    module: str
    config: Dict[str, Any] = Field(default_factory=dict)
    enable_mlflow: bool = False


class PipelineConfig(BaseModel):
    """Root pipeline configuration."""

    pipeline: List[StageConfig]

