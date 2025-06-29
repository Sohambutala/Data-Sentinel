from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal


class PollConfig(BaseModel):
    polling_path: str
    poll_type: Literal["FILE"] = "FILE"  # enforce accepted types
    max_workers: int = Field(gt=0, description="Maximum number of worker pods",default=1)

class PipelineConfig(BaseModel):
    poll: PollConfig