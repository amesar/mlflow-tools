# MLflow Display Tools 

## Overview

Tools to list and dump MLflow objects.

**List Tools**
* [Count of all MLflow objects](#Count-of-all-MLflow-objects)
* [List all experiments](#List-all-experiments)
* [List all registered models](#List-all-registered-models)
* Advanced
  * [List latest and all versions of a registered model](#List-latest-and-all-versions-of-a-registered-model) - List versions and information about the runs they point to.

**Dump Tools**
* [Samples of dumps](../../samples/README.md)
* [Dump experiment](#Dump-experiment) 
  * [Dump experiment runs to CSV file](#Dump-experiment-runs-to-CSV-file)
* [Dump registered model](#Dump-registered-model)
* [Dump run](#Dump-run)


## Setup
```
export MLFLOW_TRACKING_URI=http://localhost:5000
```

## Count of all MLflow objects
See [count_objects.py](count_objects.py).

**Example**

```
count-objects --csv_file experiments.csv
```

```
MLflow object counts
+--------------------+---------+
| Object             |   Count |
|--------------------+---------|
| experiments        |       3 |
| models             |       3 |
| versions           |       9 |
| versions by models |       9 |
+--------------------+---------+
```

**Usage**
```
count-objects --help

Options:
  --experiments         Experiments count
  --models              Registered models count
  --versions            Model versions count
  --versions-by-models  Model versions by models count
  --mlflow-api TEXT     MLflowApi implementation: iterator|list  [default:
                        iterator]
```

## Experiments 

### List all experiments
See [list_experiments.py](list_experiments.py).

**Example**

```
list-experiments --csv_file experiments.csv
```
```
+-----------------+---------------+---------------------+---------------------+-------------------+-----------------------------+
|   experiment_id | name          | creation_time       | last_update_time    | lifecycle_stage   | artifact_location           |
+-----------------+---------------+---------------------+---------------------+-------------------+-----------------------------+
|               3 | hello_world   | 2023-02-12 03:26:23 | 2023-02-12 05:36:54 | deleted           | /opt/mlflow/server/mlruns/3 |
|               4 | sparkml_scala | 2023-02-12 03:51:07 | 2023-02-12 03:51:07 | active            | /opt/mlflow/server/mlruns/4 |
|               2 | sklearn_iris  | 2023-02-08 02:13:32 | 2023-02-08 02:13:32 | active            | /opt/mlflow/server/mlruns/2 |
|               1 | sklearn_wine  | 2023-02-08 02:04:13 | 2023-02-08 02:04:13 | active            | /opt/mlflow/server/mlruns/1 |
|               0 | Default       | 2023-02-08 02:04:09 | 2023-02-08 02:04:09 | active            | /opt/mlflow/server/mlruns/0 |
+-----------------+---------------+---------------------+---------------------+-------------------+-----------------------------+
```

**Usage**
```
list-experiments --help

Options:
  --csv-file TEXT    Output CSV file.  [default: experiments.csv]
  --sort-attr TEXT   Sort by this attibute.  [default: name]
  --sort-order TEXT  Sort order. One of: asc|desc.  [default: asc]
  --view-type TEXT   View type. One of: active_only|deleted_only|all.
                     [default: active_only]
  --filter TEXT      Filter
```

### Dump experiment 

Dumps all experiment details including its runs as JSON or YAML.
* Source: [dump_experiment.py](dump_experiment.py)
* Samples:
  * Open source MLflow: 
    [experiment.json](../../samples/oss_mlflow/experiments/experiment.json) \-
    [experiment.yaml](../../samples/oss_mlflow/experiments/experiment.yaml) \-
    [experiment.txt](../../samples/oss_mlflow/experiments/experiment.txt).
  * Databricks MLflow: 
    [sklearn_wine_quality.json](../../samples/databricks_mlflow/experiments/sklearn_wine_quality.json) \-
    [sklearn_wine_quality_autolog.json](../../samples/databricks_mlflow/experiments/sklearn_wine_quality_autolog.json)
  

**Example**
```
dump-experiment \
  --experiment-id-or-name 1812 \
  --artifact-max-level 3 \
  --show-runs True \
  --show-run-data True \
  --format json
```

```
{
  "experiment_info": {
    "experiment_id": "2",
    "name": "sklearn_wine",
    "artifact_location": "/opt/mlflow/server/mlruns/2",
    "lifecycle_stage": "active",
    "last_update_time": 1673530308830,
    "creation_time": 1673530308830,
    "tags": [
      {
        "key": "version_mlflow",
        "value": "2.1.1"
      }
    ]
  },
  "summary": {
    "runs": 1,
    "artifacts": 6,
    "artifact_bytes": 31767,
    "last_run": 1673530308926,
    "_last_run": "2023-01-12 13:31:49"
  },```
  "runs": [
    {
      "summary": {
        "artifacts": 6,
        "artifact_bytes": 31767,
        "params": 2,
        "metrics": 3,
        "tags": 18
      },
      "run": {
        "info": {
          "experiment_id": "2",
          "artifact_uri": "/opt/mlflow/server/mlruns/2/e128c31217fe4e8d92d8256ca24dc28e/artifacts",
          . . .
          "lifecycle_stage": "active",
          "run_id": "e128c31217fe4e8d92d8256ca24dc28e",
        },
. . .
```

**Usage**

```
dump-experiment --help

Options:
  --experiment-id-or-name TEXT   Experiment ID or name  [required]
  --artifact-max-level INTEGER   Number of artifact levels to recurse
                                 [default: 1]
  --show-runs BOOLEAN            Show runs  [default: False]
  --show-run-data BOOLEAN        Show run data run if showing runs  [default:
                                 False]
  --format TEXT                  Output format: json|yaml|txt  [default: json]
  --explode-json-string BOOLEAN  Explode attributes that are a JSON string
                                 [default: False]
  --output-file TEXT             Output file (extension will be the format)
  --verbose BOOLEAN              Verbose
```

### Dump experiment runs to CSV file

Create a CSV file of an experiment's runs from call to [mlflow.search_runs](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.search_runs). If argument `csv_file` is not specified the output file name will be `experiment_{EXPERIMENT_ID}.csv`.
```
python -m mlflow_tools.tools.dump_experiment_as_csv \
  --experiment-id-or-name sklearn \
  --csv-file sklearn.csv
```

## Runs 

### Dump run

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
dump-run --run-id 4af184e8527a4f4a8fc563386807acb2 \
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
dump-run --help

Options:
  --run-id TEXT                  Run ID.  [required]
  --artifact-max-level INTEGER   Number of artifact levels to recurse.
  --format TEXT                  Output Format: json|yaml|txt.
  --explode-json-string BOOLEAN  Explode JSON string.  [default: False]
  --verbose BOOLEAN              Verbose.
```

## Registered models 

### List all registered models
See [list_registered_models.py](list_registered_models.py).


**Example**
```
list-models --csv_file models.csv
```
```
+--------------+------------+----------------------+--------------------------+---------------------------+
| name         |   versions | creation_timestamp   | last_updated_timestamp   | description               |
|--------------+------------+----------------------+--------------------------+---------------------------|
| sklearn_iris |          2 | 2023-01-01 19:33:02  | 2023-01-02 04:31:08      |                           |
| sklearn_wine |          1 | 2023-01-01 19:31:28  | 2023-01-16 04:34:42      | Skearn Wine Quality model |
|--------------+------------+----------------------+--------------------------+---------------------------|
```

**Usage**
```
list-models --help

Options:
  --csv-file TEXT    Output CSV file  [default: experiments.csv]
  --sort-attr TEXT   Sort by this attibute  [default: name]
  --sort-order TEXT  Sort order: asc|desc  [default: asc]
```

### Dump registered model

Dumps a registered model (as JSON and YAML) and optionally the run details of each of its versions.
* Source code: [dump_model.py](dump_model.py).
* JSON examples: [Open source MLflow](../../samples/oss_mlflow/models/registered_model.json) - [Databricks MLflow](../../samples/databricks_mlflow/models/registered_model.json).

#### Dump only registered model
```
dump-model --model sklearn_wine 
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

#### Dump registered model with version run details
```
dump-model --model sklearn_wine --show-runs
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
          }
        ],
        "params": [
          {
            "key": "max_depth",
            "value": "4"
          }
        ],
        "tags": [
          {
            "key": "mlflow.source.git.commit",
            "value": "a82570aadbd19b8736a097ea23eded98b7c42a43"
          },
          . . .
        ]
      }
    }
  }
}
```

**Usage**
```
dump-model --help

Options:
  --format TEXT                  Output format: json|yaml.
  --model TEXT                   Registered model name.  [required]
  --show-runs BOOLEAN            Show run details.  [default: False]
  --format-datetime BOOLEAN      Show human-readable datetime formats.
                                 [default: False]
  --explode-json-string BOOLEAN  Explode JSON string.  [default: False]
  --artifact-max-level INTEGER   Number of artifact levels to recurse.
                                 [default: 0]
  --show-all-versions BOOLEAN    Dump all versions in addition to latest
                                 versions.  [default: False]
```

### List `latest` and `all` versions of a registered model

List versions and information about the runs they point to.

Lists two views of versions:
  *  Latest versions use [MlflowClient.get_latest_versions()](https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.get_latest_versions).
  * All versions use [MlflowClient.search_model_versions()](https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.search_model_versions).

See [list_model_versions_advanced.py](list_model_versions_advanced.py).


```
list-model-versions_advanced \
  --model all \
  --view both 

Latest 6 versions
+-------------------+-----------+------------+---------------------+----------------------------------+-------------+--------------+
| Model             |   Version | Stage      | Creation            | Run ID                           | Run stage   | Run exists   |
|-------------------+-----------+------------+---------------------+----------------------------------+-------------+--------------|
| sklearn_iris      |         1 | None       | 2022-08-15 03:16:39 | f3bd1fd16aab4af083536002b0ae8a22 | deleted     | True         |
| sklearn_iris      |         2 | Staging    | 2022-08-15 03:16:52 | 57a185d83e2c4a6587166a56762035ab | active      | True         |
| sklearn_iris      |         3 | Archived   | 2022-08-15 03:17:04 | 5247956e9ebc4d808c11af38e3ad781e | active      | True         |
| sklearn_iris      |         5 | Production | 2022-08-15 03:23:27 | 527275d8481e4954a141ef22c919851f | deleted     | True         |
| sklearn_wine      |         2 | None       | 2022-08-15 03:19:15 | ff2e2185944d4bdeb084fab41dd240bf | active      | True         |
| sklearn_wine_onnx |         2 | None       | 2022-08-15 03:19:16 | ff2e2185944d4bdeb084fab41dd240bf | active      | True         |
+-------------------+-----------+------------+---------------------+----------------------------------+-------------+--------------+

All 9 versions
+-------------------+-----------+------------+---------------------+----------------------------------+-------------+--------------+
| Model             |   Version | Stage      | Creation            | Run ID                           | Run stage   | Run exists   |
|-------------------+-----------+------------+---------------------+----------------------------------+-------------+--------------|
| sklearn_iris      |         1 | None       | 2022-08-15 03:16:39 | f3bd1fd16aab4af083536002b0ae8a22 | deleted     | True         |
| sklearn_iris      |         2 | Staging    | 2022-08-15 03:16:52 | 57a185d83e2c4a6587166a56762035ab | active      | True         |
| sklearn_iris      |         3 | Archived   | 2022-08-15 03:17:04 | 5247956e9ebc4d808c11af38e3ad781e | active      | True         |
| sklearn_iris      |         4 | Production | 2022-08-15 03:17:37 | e9de914e80f944fda5f10e0be4ec9e3f | active      | True         |
| sklearn_iris      |         5 | Production | 2022-08-15 03:23:27 | 527275d8481e4954a141ef22c919851f | deleted     | True         |
| sklearn_wine      |         1 | None       | 2022-08-15 03:19:08 | d702d6034879405f87e4b11a38f48bee | active      | True         |
| sklearn_wine      |         2 | None       | 2022-08-15 03:19:15 | ff2e2185944d4bdeb084fab41dd240bf | active      | True         |
| sklearn_wine_onnx |         1 | None       | 2022-08-15 03:19:10 | d702d6034879405f87e4b11a38f48bee | active      | True         |
| sklearn_wine_onnx |         2 | None       | 2022-08-15 03:19:16 | ff2e2185944d4bdeb084fab41dd240bf | active      | True         |
+-------------------+-----------+------------+---------------------+----------------------------------+-------------+--------------+
```

**Usage**
```
list-model-versions-advanced --help

Options:
  --model TEXT           Registered model name or 'all' for all models.
                         [required]

  --view TEXT            Display latest, all or both views of versions. Values
                         are: 'latest|all|both'.  [default: latest]

  --max-results INTEGER  max_results parameter to
                         MlflowClient.list_registered_models().  [default:
                         1000]
```
