# Data-Sentinel

Data-Sentinel provides a pluggable orchestration framework for building
simple data workflows. The order of execution is defined in a JSON
configuration file validated using Pydantic models. Each stage of the
pipeline can receive its own configuration options.

## Example usage

```bash
python -m data_sentinel.run example_config.json
```

The configuration file contains a list of stages with optional parameters:

```json
{
  "pipeline": [
    {"module": "data_sentinel.modules.readers.RealTimeReader", "config": {"records": [4, 5, 6]}},
    {"module": "data_sentinel.modules.dq.DataQualityModule", "config": {"allow_empty": false}}
  ]
}
```
