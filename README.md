# mlflow-tools

Some useful tools for MLflow.

## Overview

### Basic Tools
 [Basic Tools README](mlflow_tools/tools/README.md)
* List all experiments
* Dump experiment as text
* Dump run as text
* Dump experiment runs as CSV file
* Find best run of an experiment
* Dump registered model as JSON or YAML
* Find matching artifacts

### Advanced Tools
* [Failed Run Replayer](mlflow_tools/failed_run_replayer) - Save run details for MLflow rate limited exceptions and replay later.

### MLflow Spark UDF Workaound
* Problem
  * Currently you cannot load a SparkML model as a UDF with MLflow due to named column bug.
  * Error message: pyspark.sql.utils.IllegalArgumentException: sepal_length does not exist. Available: 0, 1, 2, 3
  * [mlflow git issue 4131](https://github.com/mlflow/mlflow/issues/4131) - Spark UDF throws IllegalArgumentException
* Solution
  * There is a workaround that leverages a custom PythonModel wrapper.
  * Wrapper: [sparkml_udf_workaround.py](mlflow_tools/spark/sparkml_udf_workaround.py)
  * Usage: [test_sparkml_udf_workaround.py](tests/spark/test_sparkml_udf_workaround.py)


## Setup 

```
python -m venv mlflow-tools-env
source mlflow-tools-env/bin/activate
pip install -e .
```

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


