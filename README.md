# mlflow-tools

Some useful tools for MLflow.

## Overview
* [Tools](mlflow_tools/tools/README.md) - Basic tools
  * List all experiments.
  * Dump experiment and run details recursively.
  * Find the best run for an experiment
* [Export and import experiments](mlflow_tools/export_import/README.md)
  * Export experiment to a directory or zip file.
  * Import experiment from a directory or zip file.
  * Copy experiment from one MLflow tracking server to another.

## Build Wheel
```
python setup.py bdist_wheel
```
Creates `dist/mlflow_tools-0.0.1-py3-none-any.whl`.

