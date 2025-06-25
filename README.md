# Data-Sentinel

Data-Sentinel provides a pluggable orchestration framework for building
simple data workflows. The order of execution is defined in a JSON

configuration file parsed via a **Pydantic** model. The orchestrator
uses **Prefect** for task execution and individual tasks can opt in to
**MLflow** tracking via their configuration.

## Example usage

```bash
python -m data_sentinel.run example_config.json
```


The configuration file contains a list of stages with optional parameters:

```json
{
  "pipeline": [
    {"module": "data_sentinel.modules.readers.RealTimeReader"},
    {
      "module": "data_sentinel.modules.dq.DataQualityModule",
      "enable_mlflow": true
    }
  ]
}
```

When ``enable_mlflow`` is ``true`` on a pipeline stage, that task is run
inside an MLflow tracking context while Prefect continues to monitor the
overall workflow.