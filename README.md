# mlflow-tools

Some useful tools for MLflow.

## Overview

[Tools](mlflow_tools/tools/README.md) - Basic tools
* List all experiments
* Dump experiment as text
* Dump run as text
* Dump experiment runs as CSV file
* Find best run of an experiment
* Dump registered model as JSON or YAML

[Export and import](mlflow_tools/export_import/README.md)
* Export run, experiment or registered model to a directory.
* Import run, experiment or registered model from a directory.
* Copy run or experiment from one MLflow tracking server to another.

Model serving
  * [Serve MLflow Keras model with TensorFlow Serving](mlflow_tools/tensorflow_serving)

## Setup 

**Conda environment**

```
conda env create conda.yaml
source activate mlflow-tools
```

**Build Wheel**

Build wheel as `dist/mlflow_tools-0.0.1-py3-none-any.whl`.

```
python setup.py bdist_wheel
```


## Sample Run


```
export MLFLOW_TRACKING_URI=http://localhost:5000

python -m mlflow_tools.tools.best_run --experiment_id 2 --metric rmse --ascending 
```
