# Data-Sentinel

Data-Sentinel provides a pluggable orchestration framework for building
simple data workflows. The order of execution is defined in a JSON
configuration file. The orchestrator now uses **Prefect** to manage the
pipeline execution and wraps the run in an **MLflow** tracking context so
model training stages can be logged automatically.

## Example usage

```bash
python -m data_sentinel.run example_config.json
```
