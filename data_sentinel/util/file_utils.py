
from abc import ABC
import json
from pathlib import Path


def load_json_to_object(path: str | Path, class_type: ABC ) -> ABC:
    with open(path, "r", encoding="utf-8") as fh:
        cfg_dict = json.load(fh)
    return class_type(**cfg_dict)
