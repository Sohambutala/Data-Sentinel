from __future__ import annotations

import sys
from pathlib import Path

from .orchestrator import Orchestrator, load_config


def main(argv: list[str] | None = None) -> None:
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: python -m data_sentinel.run <config_file>")
        raise SystemExit(1)
    config_file = Path(argv[0])
    stages = load_config(config_file)
    orchestrator = Orchestrator(stages)
    result = orchestrator.run()
    print(result)


if __name__ == "__main__":
    main()
