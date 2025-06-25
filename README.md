# Data-Sentinel

Data-Sentinel provides a pluggable orchestration framework for building
simple data workflows. The order of execution is defined in a JSON
configuration file. The orchestrator now uses **Prefect** to manage the
pipeline execution. If ``enable_mlflow`` is set to ``true`` in the
configuration, the run is wrapped in an **MLflow** tracking context so model
training stages can be logged automatically.

## Example usage

```bash
python -m data_sentinel.run example_config.json
```

With ``enable_mlflow`` enabled, MLflow will track the pipeline run and record any metrics produced by training modules.
