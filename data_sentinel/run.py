from __future__ import annotations

import sys
from pathlib import Path

from util.file_utils import load_config
from orchestrator import Orchestrator
from config.config import PipelineConfig

def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python -m data_sentinel.run <config_file>")
        raise SystemExit(1)
    config_file = Path(argv[0])
    cfg = load_config(config_file, PipelineConfig)
    print(f"Loaded configuration from {cfg}")
    orchestrator = Orchestrator(cfg.pipeline)
    result = orchestrator.run()
    print(result)


if __name__ == "__main__":
    main()
