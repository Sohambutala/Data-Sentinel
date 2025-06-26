
def load_config(path: str | Path, type: ABC ) -> PipelineConfig:
    with open(path, "r", encoding="utf-8") as fh:
        cfg_dict = json.load(fh)
    return PipelineConfig(**cfg_dict)
