# mlflow-tools

Some useful tools for MLflow.

## Overview

Model serving
  * [Serve MLflow Keras model with TensorFlow Serving](mlflow_tools/tensorflow_serving)

[Tools](mlflow_tools/tools/README.md) - Basic tools
* List all experiments
* Dump experiment as text
* Dump run as text
* Dump experiment runs as CSV file
* Find best run of an experiment
* Dump registered model as JSON or YAML
* Find matching artifacts

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


