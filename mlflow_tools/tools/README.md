# Basic MLflow Tools 

## Overview

Some useful tools for MLflow. Run the examples from the root of repository.

**Dumps**
* [Samples of dumps](../../samples/README.md)
* [List all experiments](#List-all-experiments)
* [Dump run](#Dump-run)
* [Dump experiment](#Dump-experiment) 
  * [Dump experiment runs to CSV file](#Dump-experiment-runs-to-CSV-file)

**Registered model**
* [Register a run's model as a registered model version and optional stage](#Register-a-run's-model-as-a-registered-model-version-and-optional-stage)
* [Delete registered model](#Delete-registered-model)
* [Delete model stages](#Delete-model-stages)
* [Dump registered model](#Dump-registered-model)
* [List versions of a registered model](#List-versions-of-a-registered-model-as-text-table)
* [List all model versions and their backing run](#List-all-model-versions-and-their-backing-run)

**Other**
* [Find best run of experiment](#Find-best-run-of-experiment)
* [Find matching artifacts](#Find-matching-artifacts)
* [Download model artifacts](#Download-model-artifacts)
* [Call MLflow model server](#Call-MLflow-model-server)
* [Call http_client either MLflow API or Databricks API](#Call-http_client-either-MLflow-API-or-Databricks-API)

## Setup
```
export MLFLOW_TRACKING_URI=http://localhost:5000
```

## List all experiments
See [list_experiments.py](list_experiments.py).
```
python -m mlflow_tools.tools.list_experiments --csv_file my_experiments.csv
```
```
+----+-----------------+------------------+
|    |   experiment_id | name             |
|----+-----------------+------------------|
|  0 |               0 | Default          |
|  1 |               1 | hello_world      |
|  2 |               4 | keras_tensorflow |
|  3 |               3 | pyspark_wine     |
|  4 |               6 | scala_HelloWorld |
|  5 |               5 | scala_wine       |
|  6 |               2 | sklearn_wine     |
+----+-----------------+------------------+
```

## Dump run

Dumps run information.
* [dump_run.py](dump_run.py).
* Shows info, params, metrics and tags.
* Recursively shows all artifacts up to the specified level.
* A large value for `artifact_max_level` will execute many API calls.
* If `show-info` is true, then just the run infos will be dumped.
* If `show-data` is true, then an API call for each run will be executed. Beware of experiments with many runs.
* Samples:
  * Open source MLflow
  [run.json](../../samples/oss_mlflow/run.json), 
  [run.yaml](../../samples/oss_mlflow/run.yaml)
  and [run.txt](../../samples/oss_mlflow/run.txt).
  * Databricks MLflow 
    * Non-autolog: [run.json](../../samples/databricks_mlflow/runs/sparkml/run.json).
    * Autolog: [run_autolog.json](../../samples/databricks_mlflow/runs/sklearn_wine/run_autolog.json).

**Example**

```
python -m mlflow_tools.tools.dump_run --run-id 4af184e8527a4f4a8fc563386807acb2 \
  --artifact-max-level 5 \
  --format yaml \
  --explode-json-string True
```
```
summary:
  artifacts: 9
  artifact_bytes: 33319
  params: 2
  metrics: 3
  tags: 18
run:
  info:
    run_uuid: 4af184e8527a4f4a8fc563386807acb2
    experiment_id: '1'
    user_id: andre
    status: FINISHED
    start_time: '1629947182813'
    end_time: '1629947184041'
    artifact_uri: /opt/mlflow/server/mlruns/1/4af184e8527a4f4a8fc563386807acb2/artifacts
    lifecycle_stage: active
    run_id: 4af184e8527a4f4a8fc563386807acb2
    _start_time: '2021-08-26 03:06:22'
    _end_time: '2021-08-26 03:06:24'
    _duration: 1.228
  data:
    metrics:
    - key: rmse
      value: 0.7367947360663162
      timestamp: '1629947183157'
      step: '0'
. . .
    params:
    - key: max_depth
      value: '4'
. . .
    tags:
    - key: mlflow.user
      value: andre
    - key: mlflow.source.name
      value: main.py
. . .
artifacts:
  root_uri: /opt/mlflow/server/mlruns/1/4af184e8527a4f4a8fc563386807acb2/artifacts
  files:
  - path: onnx-model
    is_dir: true
    artifacts:
      root_uri: /opt/mlflow/server/mlruns/1/4af184e8527a4f4a8fc563386807acb2/artifacts
      files:
      - path: onnx-model/MLmodel
        is_dir: false
        file_size: '293'
      - path: onnx-model/conda.yaml
        is_dir: false
        file_size: '133'
      - path: onnx-model/model.onnx
        is_dir: false
        file_size: '1621'
      - path: onnx-model/requirements.txt
        is_dir: false
        file_size: '37'
  - path: plot.png
    is_dir: false
    file_size: '27836'
. . .

```

**Usage**

```
python -m mlflow_tools.tools.dump_run --help

Options:
  --run-id TEXT                  Run ID.  [required]
  --artifact-max-level INTEGER   Number of artifact levels to recurse.
  --format TEXT                  Output Format: json|yaml|txt.
  --explode-json-string BOOLEAN  Explode JSON string.  [default: False]
  --verbose BOOLEAN              Verbose.
```

## Dump experiment 

Dumps all experiment details including its run information as JSON, YAML or text.
* [dump_experiment.py](dump_experiment.py)
* Samples:
  * Open source MLflow: 
    [experiment.json](../../samples/oss_mlflow/experiment.json) \-
    [experiment.yaml](../../samples/oss_mlflow/experiment.yaml) \-
    [experiment.txt](../../samples/oss_mlflow/experiment.txt).
  * Databricks MLflow: 
    [sklearn_wine_quality.json](../../samples/databricks_mlflow/experiments/sklearn_wine_quality.json) \-
    [sklearn_wine_quality_autolog.json](../../samples/databricks_mlflow/experiments/sklearn_wine_quality_autolog.json)
  

**Example**

```
python -m mlflow_tools.tools.dump_experiment \
   --experiment-id-or-name sklearn_wine \
  --show-info True \
  --show-data True \
  --artifact-max-level 10 \
  --format yaml \
  --explode-json-string True
```
```
experiment_info:
  experiment_id: '1'
  name: sklearn
  artifact_location: /opt/mlflow/server/mlruns/1
  lifecycle_stage: active
  tags:
  - key: mlflow.note.content
    value: Hello experiment
summary:
  runs: 2
  artifacts: 18
  artifact_bytes: 66638
  last_run: 1630006099305
  _last_run: '2021-08-26 19:28:19'
runs:
- summary:
    artifacts: 9
    artifact_bytes: 33319
    params: 2
    metrics: 3
    tags: 17
  run:
    info:
      run_uuid: b2a34eb3d1f245c68e3586beb6912bc1
      experiment_id: '1
. . .
```

**Usage**

```
python -m mlflow_tools.tools.dump_experiment --help

Options:
  --experiment-id-or-name TEXT   Experiment ID or name  [required]
  --artifact-max-level INTEGER   Number of artifact levels to recurse
  --show-info BOOLEAN            Show run info  [default: False]
  --show-data BOOLEAN            Show data run info and data  [default: False]
  --format TEXT                  Output format: json|yaml|txt
  --explode-json-string BOOLEAN  Explode JSON string  [default: False]
  --verbose BOOLEAN              Verbose
```

## Dump experiment runs to CSV file

Create a CSV file of an experiment's runs from call to [mlflow.search_runs](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.search_runs). If argument `csv_file` is not specified the output file name will be `experiment_{EXPERIMENT_ID}.csv`.
```
python -m mlflow_tools.tools.dump_experiment_as_csv \
  --experiment-id-or-name sklearn \
  --csv-file sklearn.csv
```


## Find best run of experiment

Find the best run for a metric of an experiment. 
Default order is descending (max). See [best_run.py](best_run.py).

Displays the run ID and best metric value.

```
python -m mlflow_tools.tools.best_run --experiment-id-or-nam 2 --metric rmse --ascending True
```
```
Best run:
  run_id: 7890e3ec549442ebae453394ea7dd1ea
  rmse: 0.8829449794492825
```

**Usage**

```
python -m mlflow_tools.tools.best_run --help

Options:
  --experiment-id-or-name TEXT  Experiment ID or name.  [required]
  --metric TEXT                 Metric.  [required]
  --ascending BOOLEAN           Sort ascending.  [default: False]
  --ignore-nested-runs BOOLEAN  Ignore_nested_runs.  [default: False]
```


## Find matching artifacts

Return artifact paths that match specified target filename.

**Example**

```
python -m mlflow_tools.tools.find_artifacts \
  --run-id 4af184e8527a4f4a8fc563386807acb2 \
  --target MLmodel
```
```
Matches:
  onnx-model/MLmodel
  sklearn-model/MLmodel
```

**Usage**
```
python -m mlflow_tools.tools.find_artifacts --help

Options:
  --run-id TEXT        Run ID.  [required]
  --path TEXT          Relative artifact path.  [default: ]
  --target TEXT        Target filename to search for.  [required]
  --max-level INTEGER  Number of artifact levels to recurse.  [default: 9223372036854775807]
```

## Download model artifacts

Download the model artifacts associated with a model URI.

```
python -m mlflow_tools.tools.download_model \
   --model-uri models:/sklearn_wine \
   --output-dir /tmp/my-model
```

```
python -m mlflow_tools.tools.download_model \
   --model-uri runs:/18f6b9a2f72f44de8bb9591d163c6754/sklearn-model \
   --output-dir /tmp/my-model
```

```
+-sklearn-model/
  +-requirements.txt
  +-model.pkl
  +-conda.yaml
  +-MLmodel
```

**Usage**
```
python -m mlflow_tools.tools.download_model --help

Options:
  --model-uri TEXT   Model URI  [required]
  --output-dir TEXT  Output directory for downloaded model  [required]
```


## Call MLflow model server

Invoke the MLflow model server to score wine quality file.

Invoke open source MLfow model server.
```
python -m mlflow_tools.tools.call_model_server \
   --api-uri http://localhost:5001/invocations \
   --datapath wine-quality-split-orient.json
```

Invoke Databricks MLfow model server.
```
python -m mlflow_tools.tools.call_model_server \
   --api-uri https://my-workspace.mycompany.com/model-endpoint/Sklearn_Train_Predict/1/invocations \
   --datapath wine-quality-split-orient.json \
   --token MY_TOKEN
```

## Register a run's model as a registered model version and optional stage

```
python -m mlflow_tools.tools.register_model \
  --registered-model my-registered-model \
  --run-id 123 \
  --model-artifact my-model \
  --stage production
```

**Usage**
```
python -m mlflow_tools.tools.register_model --help

Options:
  --registered-model TEXT  New registered model name.  [required]
  --run-id TEXT            Run ID  [required]
  --model-artifact TEXT    Source relative model artifact path.  [required]
  --stage TEXT             Stage
```

## Delete registered model 
```
python -m mlflow_tools.tools.delete_model --model sklearn_wine
```
**Usage**
```
python -m mlflow_tools.tools.delete_model --help

Options:
  --model MODEL  Registered model name
```
## Delete model stages

Delete model stages.

```
python -m mlflow_tools.tools.delete_model_stages \
  --model sklearn_wine \
  --stages None,Archived
```

**Usage**
```
Options:
  --model TEXT   Registered model name  [required]
  --stages TEXT  Stages to export (comma seperated). Default is all stages.
```
## Dump registered model

Dumps a registered model (as JSON and YAML) and optionally the run details of each of its versions.
* JSON examples: [Open source MLflow](../../samples/oss_mlflow/registered_model.json) - [Databricks MLflow](../../samples/databricks_mlflow/models/registered_model.json).
* Source code: [dump_model.py](dump_model.py).

### Dump only registered model
```
python -m mlflow_tools.tools.dump_model --model sklearn_wine 
```
```
{
  "registered_model": {
    "name": "sklearn_wine",
    "creation_timestamp": "1584980474711",
    "last_updated_timestamp": "1584980474738",
    "latest_versions": [
      {
        "name": "e2e-ml-pipeline",
        "version": "1",
        "creation_timestamp": "1584980474738",
        "last_updated_timestamp": "1584980474738",
        "current_stage": "Production",
        "source": "file:///opt/mlflow/server/mlruns/5/bd19af4c8b67420e8371bbe5b6982402/artifacts/sklearn-model",
        "run_id": "bd19af4c8b67420e8371bbe5b6982402",
        "status": "READY"
      }
    ]
  }
}
```

### Dump registered model with run details
```
python -m mlflow_tools.tools.dump_model --model sklearn_wine --show_runs
```
```
{
  "model": {
    "registered_model": {
      "name": "e2e-ml-pipeline",
      "creation_timestamp": "1584980474711",
      "last_updated_timestamp": "1584980474738",
      "latest_versions": [
        {
          "name": "e2e-ml-pipeline",
          "version": "1",
          "creation_timestamp": "1584980474738",
          "last_updated_timestamp": "1584980474738",
          "current_stage": "Production",
          "source": "file:///opt/mlflow/server/mlruns/1812/bd19af4c8b67420e8371bbe5b6982402/artifacts/sklearn-model",
          "run_id": "bd19af4c8b67420e8371bbe5b6982402",
          "status": "READY"
        }
      ]
    }
  },
  "version_runs": {
    "1": {
      "info": {
        "run_uuid": "bd19af4c8b67420e8371bbe5b6982402",
        "experiment_id": "1812",
        "user_id": "andre",
        "status": "FINISHED",
        "start_time": "1584980474016",
        "end_time": "1584980479782",
        "artifact_uri": "file:///opt/mlflow/server/mlruns/1812/bd19af4c8b67420e8371bbe5b6982402/artifacts",
        "lifecycle_stage": "active",
        "run_id": "bd19af4c8b67420e8371bbe5b6982402"
      },
      "data": {
        "metrics": [
          {
            "key": "mae",
            "value": 0.5866345750858584,
            "timestamp": "1584980474565",
            "step": "0"
          },
          {
            "key": "r2",
            "value": 0.2543237115463549,
            "timestamp": "1584980474546",
            "step": "0"
          },
          {
            "key": "rmse",
            "value": 0.7642618555591052,
            "timestamp": "1584980474518",
            "step": "0"
          }
        ],
        "params": [
          {
            "key": "max_depth",
            "value": "4"
          },
          {
            "key": "max_leaf_nodes",
            "value": "32"
          }
        ],
        "tags": [
          {
            "key": "data_path",
            "value": "../../data/wine-quality-white.csv"
          },
          {
            "key": "mlflow.log-model.history",
            "value": "[{\"run_id\": \"bd19af4c8b67420e8371bbe5b6982402\", \"artifact_path\": \"sklearn-model\", \"utc_time_created\": \"2020-03-23 16:21:14.622448\", \"flavors\": {\"python_function\": {\"loader_module\": \"mlflow.sklearn\", \"python_version\": \"3.7.5\", \"data\": \"model.pkl\", \"env\": \"conda.yaml\"}, \"sklearn\": {\"pickled_model\": \"model.pkl\", \"sklearn_version\": \"0.19.2\", \"serialization_format\": \"cloudpickle\"}}}, {\"run_id\": \"bd19af4c8b67420e8371bbe5b6982402\", \"artifact_path\": \"onnx-model\", \"utc_time_created\": \"2020-03-23 16:21:17.799155\", \"flavors\": {\"python_function\": {\"loader_module\": \"mlflow.onnx\", \"python_version\": \"3.7.5\", \"data\": \"model.onnx\", \"env\": \"conda.yaml\"}, \"onnx\": {\"onnx_version\": \"1.6.0\", \"data\": \"model.onnx\"}}}]"
          },
          {
            "key": "mlflow.runName",
            "value": "train.sh"
          },
          {
            "key": "mlflow.source.git.commit",
            "value": "a82570aadbd19b8736a097ea23eded98b7c42a43"
          },
          {
            "key": "mlflow.source.name",
            "value": "main.py"
          },
          {
            "key": "mlflow.source.type",
            "value": "LOCAL"
          },
          {
            "key": "mlflow.user",
            "value": "andre"
          },
          {
            "key": "mlflow_version",
            "value": "1.7.0"
          },
          {
            "key": "onnx_version",
            "value": "1.6.0"
          }
        ]
      }
    }
  }
}
```

**Usage**
```
python -m mlflow_tools.tools.dump_model --help

Options:
  --format TEXT                  Output format: json|yaml.
  --model TEXT                   Registered model name.  [required]
  --show-runs BOOLEAN            Show run details.
  --format-datetime BOOLEAN      Show human-readable datetime formats.
  --explode-json-string BOOLEAN  Explode JSON string.  [default: False]
  --artifact-max-level INTEGER   Number of artifact levels to recurse.
```


## List versions of a registered model

Lists two views of versions:
  *  Latest versions use [MlflowClient.get_latest_versions()](https://mlflow.org/docs/latest/python_api/mlflow.tracking.html#mlflow.tracking.MlflowClient.get_latest_versions).
  * All versions use [MlflowClient.search_model_versions()](https://mlflow.org/docs/latest/python_api/mlflow.tracking.html#mlflow.tracking.MlflowClient.search_model_versions).

See [list_model_versions.py](list_model_versions.py).

```
python -m mlflow_tools.tools.list_model_versions --model sklearn_wine
```

```
Model: sklearn_iris

Latest 4 versions
+-----------+------------+----------+---------------------+
|   Version | Stage      | Status   | Creation            |
|-----------+------------+----------+---------------------|
|        25 | Staging    | READY    | 2022-08-05 17:44:27 |
|        23 | Production | READY    | 2022-08-05 17:43:55 |
|        28 | None       | READY    | 2022-08-07 01:17:14 |
|        24 | Archived   | READY    | 2022-08-05 17:44:10 |
+-----------+------------+----------+---------------------+

All 5 versions
+-----------+------------+----------+---------------------+
|   Version | Stage      | Status   | Creation            |
|-----------+------------+----------+---------------------|
|        25 | Staging    | READY    | 2022-08-05 17:44:27 |
|        23 | Production | READY    | 2022-08-05 17:43:55 |
|        26 | None       | READY    | 2022-08-05 17:44:42 |
|        28 | None       | READY    | 2022-08-07 01:17:14 |
|        24 | Archived   | READY    | 2022-08-05 17:44:10 |
+-----------+------------+----------+---------------------+
```

## List all model versions and their backing run
## List versions and their backing run for all registered models

List all versions of all registered models with emphasis on if the version's backing run exists.

Uses [MlflowClient.search_model_versions()](https://mlflow.org/docs/latest/python_api/mlflow.tracking.html#mlflow.tracking.MlflowClient.search_model_versions).

See [list_all_model_versions.py](list_all_model_versions.py).

```
python -m mlflow_tools.tools.list_all_model_versions
```

```
+-----------------------+-----------+-----------------+--------+-------------+--------------+
| Model                 |   Version | Version stage   | Run ID | Run stage   | Run exists   |
|-----------------------+-----------+-----------------+--------+-------------+--------------|
| Sklearn_Wine_Quality  |         2 | Production      | 1776   | active      | True         |
| Sklearn_Wine_Quality  |         1 | Staging         | 1783   | active      | True         |
| Bad_Loan_Model        |        14 | Production      | 1812   | deleted     | True         |
| Bad_Loan_Model        |         8 | Archived        | 1815   |             | False        |
| Bad_Loan_Model        |        13 | None            | 1865   |             | False        |
+-----------------------+-----------+-----------------+--------+-------------+--------------+
```

## Call http_client - either MLflow API or Databricks API

**Usage**
```
python -m mlflow_tools.common.http_client --help

Options:
  --api TEXT          API: mlflow|databricks.
  --resource TEXT     API resource such as 'experiments/list'.  [required]
  --method TEXT       HTTP method: GET|POST.
  --params TEXT       HTTP GET query parameters as JSON.
  --data TEXT         HTTP POST data as JSON.
  --output-file TEXT  Output file.
  --verbose BOOLEAN   Verbose.  [default: False]
  --help              Show this message and exit.
```

**HTTP GET example**
```
export MLFLOW_TRACKING_URI=http://localhost:5000

python -m mlflow_tools.common.http_client \
  --resource experiments/list\
  --output-file experiments.json
```

**HTTP POST example**
```
export MLFLOW_TRACKING_URI=http://localhost:5000

python -m mlflow_tools.common.http_client \
  --resource experiments/create \
  --data '{"name": "my_experiment"}'
```
