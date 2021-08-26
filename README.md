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
* Delete registered model.
* Find matching artifacts
* Download model artifacts.

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

### Seldon MLflow MLServer

Enable Seldon [MLServer](https://github.com/SeldonIO/MLServer) to support MLflow model URIs with the `models` and `runs` scheme.

Typically production MLflow pipelines deploy models using the `models` URI scheme which accesses the MLflow [Model Registry](https://mlflow.org/docs/latest/registry.html#mlflow-model-registry).

Seldon provides MLServer that supports an MLflow runtime.
However MLServer only accepts file-based MLflow model URI schems such as `s3`, `wasb`, or local file path.
MLServer does not support the `models` or `runs` schemes which download the requested model using the MLflowClient.



#### Setup

```
python -m venv mlserver
source mlserver/bin/activate

pip install mlserver
pip install mlserver-mlflow

git clone https://github.com/amesar/mlflow-tools
pip install -e mlflow-tools
```

#### Source Code

* [mlflow_tools/seldon_mlflow/download_model.py](mlflow_tools/seldon_mlflow/download_model.py)
* [mlflow_tools/common/model_download_utils.py.py](mlflow_tools/common/model_download_utils.py)

#### Create custom model-settings file

Create your settings file with an MLflow model URI using the `models` scheme.

For example, `my-model-settings.json` file.
```
{
    "name": "wine-classifier",
    "implementation": "mlserver_mlflow.MLflowRuntime",
    "parameters": {
        "uri": "models:/sklearn_wine/production"

    }
}
```

#### Download model and create model-settings.json

The [mlflow_tools.seldon_mlflow.download_model](mlflow_tools/seldon_mlflow/download_model.py) tool does the following:
  * Downloads the model artifacts associated with the registered model to a temporary location.
  * Creates a standard model-settings.json file from your custom settings file that points to this temporary location.

```

python -u -m mlflow_tools.seldon_mlflow.download_model \
  --model-settings-path my-model-settings.json \
  --output-dir /tmp/my-model
```

#### Generated model-setting.json file
```
{
    "name": "wine-classifier",
    "implementation": "mlserver_mlflow.MLflowRuntime",
    "parameters": {
        "uri": "/tmp/my-model/sklearn-model"
    }
}
```

#### Run MLServer

```
mlserver start .
```

#### Score

Score with the MLflow model server JSON format (in another terminal).
```
curl  http://localhost:8080/invocations  \
  -H "Content-Type:application/json" \
  -d '{ "columns":   
           [ "alcohol", "chlorides", "citric acid", "density", "fixed acidity", "free sulfur dioxide", "pH", "residual sugar", "sulphates", "total sulfur dioxide", "volatile acidity" ],
        "data": [
           [ 7,   0.27, 0.36, 20.7, 0.045, 45, 170, 1.001,  3,    0.45,  8.8 ],
           [ 6.3, 0.3,  0.34,  1.6, 0.049, 14, 132, 0.994,  3.3,  0.49,  9.5 ] ] }'
```
```
[5.335031847133758, 4.5]
```

## Setup 

Create a virtual environment and install package.
```
python -m venv mlflow-tools
source mlflow-tools/bin/activate
pip install -e .
```

Build a wheel in `dist/mlflow_tools-1.0.0-py3-none-any.whl`.

```
python setup.py bdist_wheel
```


