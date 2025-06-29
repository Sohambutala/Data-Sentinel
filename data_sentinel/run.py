from __future__ import annotations

import sys
from pathlib import Path

from data_sentinel.config.config import PipelineConfig
from data_sentinel.poller import Poller
from data_sentinel.util.file_utils import load_json_to_object

def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python -m data_sentinel.run <config_file>")
        raise SystemExit(1)
    config_file = Path(argv[0])
    cfg: PipelineConfig = load_json_to_object(config_file, PipelineConfig)
    print(f"Loaded configuration from {cfg}")
    orchestrator = Poller(cfg)
    result = orchestrator.run()
    print(result)


if __name__ == "__main__":
    main()
