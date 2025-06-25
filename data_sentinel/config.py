from __future__ import annotations

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class StageConfig(BaseModel):
    """Configuration for a single pipeline stage."""

    module: str
    config: Dict[str, Any] = Field(default_factory=dict)


class PipelineConfig(BaseModel):
    """Top level configuration schema."""

    pipeline: List[StageConfig]
