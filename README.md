# mlflow-tools

Some useful tools for MLflow.

## Overview

[Basic Tools](mlflow_tools/tools/README.md)
* List all experiments
* Dump experiment as text
* Dump run as text
* Dump experiment runs as CSV file
* Find best run of an experiment
* Dump registered model as JSON or YAML
* Find matching artifacts

Advanced Tools
* [Failed Run Replayer](mlflow_tools/failed_run_replayer/README.md) - Save run details for MLflow rate limited exceptions and replay later.

## Setup 

**Conda environment**

```
conda env create --file conda.yaml
conda activate mlflow-tools
```

**Build Wheel**

Build wheel as `dist/mlflow_tools-1.0.0-py3-none-any.whl`.

```
python setup.py bdist_wheel
```


