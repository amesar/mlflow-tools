# mlflow-tools

Some tools for MLflow.

## Overview

* [Dislay tools](mlflow_tools/display/README.md) - show details and list MLflow objects
  * Superceded by https://github.com/amesar/mlflow-reports. [Sample JSON output](samples/README.md)
    * Superceded by [this](https://github.com/amesar/mlflow-reports/blob/master/samples/databricks/README.md).
* [Manipulate object tools](mlflow_tools/tools/README.md) - manipulate MLflow objects - delete, rename, etc.
* [Other tools](README_other.md)
  * [Failed runs](mlflow_tools/failed_run_replayer/README.md) - Save run details for MLflow rate limited exceptions and replay later.
  * [ Model version validation tools](README_check_version.md)
* [Databricks notebooks](databricks_notebooks/README.md)
* [Tests](tests/README.md)

## MLflow Tools

### Command line scripts

#### Display (list and dump) MLflow objects

* [README](mlflow_tools/display/README.md)
* List: experiments, registered models and model versions
* Dump: run, experiment and registered model 
* [JSON samples of MLflow object display dumps](samples/README.md)

#### Model Version Validation 

* See [README_check_version](README_check_version.md).
* Tools to:
  * Validate a version's MLflow model.
  * Compare two versions' MLflow models.

#### Helper Tools
* [README](mlflow_tools/tools/README.md)
* Find best run of an experiment.
* Find model artifact paths of a run
* Find matching artifacts
* Download model artifacts.
* Call MLflow model server.
* Registered model tools
  * Register a run's model as a registered model.
  * Delete registered model.
  * Delete model stages.
* Call http_client - either MLflow API or Databricks API.

### Databricks notebooks 

* Notebook ([README](databricks_notebooks/README.md)) versions of command line scripts
* Sample notebook screenshots:
     [list registered models](samples/databricks_mlflow/notebooks/List_Models.png)
  ,  [dump model](samples/databricks_mlflow/notebooks/Dump_Model_01.png)
  and [list model versions](samples/databricks_mlflow/notebooks/Dump_Model_02.png)

### Other tools

[README](README_other.md):
* MLflow Spark UDF Workaound
* Failed Run Replayer
* Seldon MLflow MLServer


## Setup 

#### Step 1. Create a virtual environment.
```
python -m venv mlflow-tools
source mlflow-tools/bin/activate
```

#### Step 2. pip install

pip install from github
```
pip install git+https:///github.com/amesar/mlflow-tools/#egg=mlflow-tools
```

or pip install in editable mode
```
git clone https://github.com/amesar/mlflow-tools
cd mlflow-tools
pip install -e .
```
