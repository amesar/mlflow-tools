# mlflow-tools

Some useful tools for MLflow.

## Overview
* [Tools](mlflow_tools/tools/README.md) - Basic tools
  * List all experiments.
  * Dump experiment and run details recursively.
  * Find the best run for an experiment
  * Dump registered model as JSON or YAML
* [Export and import](mlflow_tools/export_import/README.md)
  * Export run, experiment or registered model to a directory.
  * Import run, experiment or registered model from a directory.
  * Copy run or experiment from one MLflow tracking server to another.

## Build Wheel
```
python setup.py bdist_wheel
```
Creates `dist/mlflow_tools-0.0.1-py3-none-any.whl`.

