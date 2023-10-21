# MLflow Display Tools 

## Overview

Tools to list and dump MLflow objects.
See also:
* [Databricks notebooks versions](../../databricks_notebooks/README.md).
* [JSON sample dumps](../../samples/README.md).


**List objects**
* [List runs](#List-runs)
* [List experiments](#List-experiments)
* [List registered models](#List-registered-models)
* [List model versions](#List-model-versions)
  * [List model versions with runs](#List-model-versions-with-runs) - list versions and their run information
* [List run or experiment tags] XX
* [Count of all MLflow objects](#Count-all-MLflow-objects)

**Dump objects**
* [Dump run](#Dump-run)
* [Dump experiment](#Dump-experiment) 
  * [Dump experiment runs to CSV file](#Dump-experiment-runs-to-CSV-file)
* [Dump registered model](#Dump-registered-model)
* [Dump registered model version](#Dump-registered-model-version)
* [Dump MLflow model](#Dump-MLflow-model) - Dump the ModelInfo of an MLflow model

**Reports**
* [Report model version](#Report-model-version) - High-level model governance report for a model version

## List objects 

### List runs

List runs of an experiment.

Source: [list_runs.py](list_runs.py).

**Example**

```
list-runs \
  --experiment-id-or-name sklearn \
  --view-type all \
  --sort-attr lifecycle_stage \
  --sort-order desc \
  --columns run_id,run_name,status,lifecycle_stage,start_time
```
```

+----------------------------------+-------------------------------------+----------+-------------------+---------------------+
| run_id                           | run_name                            | status   | lifecycle_stage   | start_time          |
|----------------------------------+-------------------------------------+----------+-------------------+---------------------|
| 79c2c0a160744c7e95956787b01d287f | 2023-03-22 22:39:36 sample.sh 2.2.2 | FINISHED | active            | 2023-03-22 22:39:36 |
| 37d4deb43f384b7486ea7919d578ceb9 | 2023-03-22 22:39:30 sample.sh 2.2.2 | FINISHED | active            | 2023-03-22 22:39:30 |
| e181dadc76524d5faa0f70bf4915253c | 2023-03-22 22:39:24 sample.sh 2.2.2 | FINISHED | active            | 2023-03-22 22:39:25 |
| 11dddd8bda8b4c6c86a2891b41a9173d | 11dddd8bda8b4c6c86a2891b41a9173d    | FINISHED | active            | 2023-03-22 21:56:28 |
| 01d0720c0bc144a1967accecaeffa031 | 01d0720c0bc144a1967accecaeffa031    | FINISHED | active            | 2023-03-21 01:33:55 |
| 7411d1f2606e4cc28c54563f25c49a02 | 7411d1f2606e4cc28c54563f25c49a02    | FINISHED | deleted           | 2023-03-21 01:33:48 |
+----------------------------------+-------------------------------------+----------+-------------------+---------------------+
```

**Usage**
```
list-runs --help

Options:
  --experiment-id-or-name TEXT  Experiment ID or name  [required]
  --sort-attr TEXT              Sort by this attr.  [default: name]
  --sort-order TEXT             Sort order. One of: asc|desc.  [default: asc]
  --view-type TEXT              View type. One of:
                                active_only|deleted_only|all.
  --columns TEXT                Columns to display (comma delimited).
  --csv-file TEXT               Output CSV file.
```

### List experiments

Source: [list_experiments.py](list_experiments.py).

**Example**

```
list-experiments \
   --csv-file experiments.csv \
   --view-type all
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
  --sort-attr TEXT   Sort by this attr.  [default: name]
  --sort-order TEXT  Sort order. One of: asc|desc.  [default: asc]
  --view-type TEXT   View type. One of: active_only|deleted_only|all.
  --filter TEXT      Filter
  --columns TEXT     Columns to display (comma delimited).
  --csv-file TEXT    Output CSV file.
```
### List registered models
Source: [list_registered_models.py](list_registered_models.py).


**Example**
```
list-registered-models --csv-file models.csv
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
  --sort-attr TEXT   Sort by this attr.  [default: name]
  --sort-order TEXT  Sort order. One of: asc|desc.  [default: asc]
  --columns TEXT     Columns to display (comma delimited).
  --csv-file TEXT    Output CSV file.
```

### List model versions 

Source: [list_model_versions.py](list_model_versions.py).

List versions using the [search_model_versions](https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.search_model_versions).

**Example**
```
list-model-versions
```

```
+-------------------+-----------+-----------------+----------+----------------------+--------------------------+----------------------------------+------------+-------------------------------------------------------------------------------+
| name              |   version | current_stage   | status   | creation_timestamp   | last_updated_timestamp   | run_id                           | run_link   | source                                                                        |
|-------------------+-----------+-----------------+----------+----------------------+--------------------------+----------------------------------+------------+-------------------------------------------------------------------------------|
| sklearn_iris      |         1 | Production      | READY    | 2023-03-04 20:37:59  | 2023-03-04 20:37:59      | b0244cc3d83b4eefaa7f43f9c0d3ed16 |            | s3://mlflow_server/2/b0244cc3d83b4eefaa7f43f9c0d3ed16/artifacts/sklearn-model |
| sklearn_wine      |         4 | None            | READY    | 2023-03-04 20:25:09  | 2023-03-04 20:25:09      | 3f8875ccef60486b9644a30c132ff586 |            | s3://mlflow_server/1/3f8875ccef60486b9644a30c132ff586/artifacts/model         |
| sklearn_wine      |         3 | Staging         | READY    | 2023-03-04 20:24:58  | 2023-03-04 20:24:58      | 7a991537ba4a4244ad2e90f26274a3da |            | s3://mlflow_server/1/7a991537ba4a4244ad2e90f26274a3da/artifacts/model         |
| sklearn_wine      |         2 | Production      | READY    | 2023-03-04 20:24:48  | 2023-03-04 20:24:48      | bfbe5e23cdbd4f43b450f2749850a2b5 |            | s3://mlflow_server/1/bfbe5e23cdbd4f43b450f2749850a2b5/artifacts/model         |
| sklearn_wine      |         1 | Archived        | READY    | 2023-03-04 20:23:36  | 2023-03-04 20:24:48      | c9ec16d723c849608f87548d65eed8a7 |            | s3://mlflow_server/1/c9ec16d723c849608f87548d65eed8a7/artifacts/model         |
| sklearn_wine_onnx |         4 | None            | READY    | 2023-03-04 20:25:12  | 2023-03-04 20:25:12      | 3f8875ccef60486b9644a30c132ff586 |            | s3://mlflow_server/1/3f8875ccef60486b9644a30c132ff586/artifacts/onnx-model    |
| sklearn_wine_onnx |         3 | None            | READY    | 2023-03-04 20:25:01  | 2023-03-04 20:25:01      | 7a991537ba4a4244ad2e90f26274a3da |            | s3://mlflow_server/1/7a991537ba4a4244ad2e90f26274a3da/artifacts/onnx-model    |
| sklearn_wine_onnx |         2 | None            | READY    | 2023-03-04 20:24:51  | 2023-03-04 20:24:51      | bfbe5e23cdbd4f43b450f2749850a2b5 |            | s3://mlflow_server/1/bfbe5e23cdbd4f43b450f2749850a2b5/artifacts/onnx-model    |
| sklearn_wine_onnx |         1 | None            | READY    | 2023-03-04 20:23:39  | 2023-03-04 20:23:39      | c9ec16d723c849608f87548d65eed8a7 |            | s3://mlflow_server/1/c9ec16d723c849608f87548d65eed8a7/artifacts/onnx-model    |
+-------------------+-----------+-----------------+----------+----------------------+--------------------------+----------------------------------+------------+-------------------------------------------------------------------------------+
```

**Usage**
```
list-model-versions --help

Options:
  --model TEXT             Registered model to filter by.
  --sort-attr TEXT         Sort by this attr.  [default: name]
  --sort-order TEXT        Sort order. One of: asc|desc.  [default: asc]
  --use-by-models BOOLEAN  Use 'by models' variant to search for versions.
  --columns TEXT           Columns to display (comma delimited).
  --csv-file TEXT          Output CSV file.
```

### List model versions with runs

List model versions and information about the version's run.

This script allows you to see if a version's run is "soft deleted" or "hard deleted".
  * Soft delete - run's `run_lifecycle_stage` column is marked as `deleted` but the run still exists in the MLflow database.
  * Hard delete (`run_exists` column) - run has physically been removed from the MLflow database. 
    * For Databricks, a run is recycled after [30 days](https://docs.databricks.com/mlflow/tracking.html#delete-runs). 
    * For OSS MLflow, the procedure to hard delete is apparently not provided and is left as an exercise to the reader.

Versions can be obtained from MLflow in two ways (option `get-latest-versions`).
  *  Latest versions use [MlflowClient.get_latest_versions()](https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.get_latest_versions).
  * All versions use [MlflowClient.search_model_versions()](https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.search_model_versions).

Source: [list_model_versions_with_runs.py](list_model_versions_with_runs.py).

_**List all 'latest' version information**_
```
list-model-versions-with-runs \
    --filter "name like 'sklearn_win%'" \
    --get_latest_versions True
```

```
8 versions - using 'latest' get mode
+-------------------+-----------+------------+---------------------+----------------------------------+--------------+-------------+---------------------+
| model             |   version | vr_stage   | vr_created          | run_id                           | run_exists   | run_stage   | run_end             |
|-------------------+-----------+------------+---------------------+----------------------------------+--------------+-------------+---------------------|
| sklearn_wine      |         3 | Archived   | 2023-03-22 21:56:30 | 11dddd8bda8b4c6c86a2891b41a9173d | True         | active      | 2023-03-22 21:56:32 |
| sklearn_wine      |         4 | Production | 2023-03-22 22:39:27 | e181dadc76524d5faa0f70bf4915253c | True         | active      | 2023-03-22 22:39:28 |
| sklearn_wine      |         5 | Staging    | 2023-03-22 22:39:32 | 37d4deb43f384b7486ea7919d578ceb9 | True         | deleted     | 2023-03-22 22:39:34 |
| sklearn_wine      |         6 | None       | 2023-03-22 22:39:38 | 79c2c0a160744c7e95956787b01d287f | True         | active      | 2023-03-22 22:39:39 |
| sklearn_wine_onnx |         3 | Archived   | 2023-03-22 21:56:31 | 11dddd8bda8b4c6c86a2891b41a9173d | True         | active      | 2023-03-22 21:56:32 |
| sklearn_wine_onnx |         4 | Production | 2023-03-22 22:39:28 | e181dadc76524d5faa0f70bf4915253c | True         | active      | 2023-03-22 22:39:28 |
| sklearn_wine_onnx |         5 | Staging    | 2023-03-22 22:39:34 | 37d4deb43f384b7486ea7919d578ceb9 | True         | deleted     | 2023-03-22 22:39:34 |
| sklearn_wine_onnx |         6 | None       | 2023-03-22 22:39:39 | 79c2c0a160744c7e95956787b01d287f | True         | active      | 2023-03-22 22:39:39 |
+-------------------+-----------+------------+---------------------+----------------------------------+--------------+-------------+---------------------+
```

_**List 'latest' production versions**_

```
list-model-versions-with-runs \
    --filter "name like 'sklearn_win%'" \
    --version-stage production \
    --get_latest_versions True
```
```
2 versions - using 'latest' get mode
+-------------------+-----------+------------+---------------------+----------------------------------+--------------+-------------+---------------------+
| model             |   version | vr_stage   | vr_created          | run_id                           | run_exists   | run_stage   | run_end             |
|-------------------+-----------+------------+---------------------+----------------------------------+--------------+-------------+---------------------|
| sklearn_wine      |         4 | Production | 2023-03-22 22:39:27 | e181dadc76524d5faa0f70bf4915253c | True         | active      | 2023-03-22 22:39:28 |
| sklearn_wine_onnx |         4 | Production | 2023-03-22 22:39:28 | e181dadc76524d5faa0f70bf4915253c | True         | active      | 2023-03-22 22:39:28 |
+-------------------+-----------+------------+---------------------+----------------------------------+--------------+-------------+---------------------+
```

_**List 'all' versions whose runs have been deleted**_
```
list-model-versions-with-runs \
    --filter "name like 'sklearn_win%'" \
    --run-lifecycle-stage deleted \
    --get_latest_versions False
```
```
4 versions - using 'all' get mode
+-------------------+-----------+------------+---------------------+----------------------------------+--------------+-------------+---------------------+
| model             |   version | vr_stage   | vr_created          | run_id                           | run_exists   | run_stage   | run_end             |
|-------------------+-----------+------------+---------------------+----------------------------------+--------------+-------------+---------------------|
| sklearn_wine      |         5 | Staging    | 2023-03-22 22:39:32 | 37d4deb43f384b7486ea7919d578ceb9 | True         | deleted     | 2023-03-22 22:39:34 |
| sklearn_wine      |         1 | Archived   | 2023-03-21 01:33:51 | 7411d1f2606e4cc28c54563f25c49a02 | True         | deleted     | 2023-03-21 01:33:52 |
| sklearn_wine_onnx |         5 | Staging    | 2023-03-22 22:39:34 | 37d4deb43f384b7486ea7919d578ceb9 | True         | deleted     | 2023-03-22 22:39:34 |
| sklearn_wine_onnx |         1 | Archived   | 2023-03-21 01:33:52 | 7411d1f2606e4cc28c54563f25c49a02 | True         | deleted     | 2023-03-21 01:33:52 |
+-------------------+-----------+------------+---------------------+----------------------------------+--------------+-------------+---------------------+
```

**Usage**
```
list-model-versions-with-runs --help

Options:
  --model-names TEXT             Model names (comma delimited)  or 'all' for
                                 all models. Mutually exclusive with 'filter'
                                 option
  --filter TEXT                  Standard filter for
                                 search_registered_models(). Mutually
                                 exclusive with 'model-names' option
  --get-latest-versions BOOLEAN  Get 'latest' versions. Otherwise get all
                                 versions.  [default: False]
  --version-stage TEXT           Show versions with specified version stage
                                 (Production, Staging, Archived).
  --run-lifecycle-stage TEXT     Show versions whose run is of specified
                                 lifecycle_stage (active, deleted).
  --columns TEXT                 Columns to display (comma delimited).
  --csv-file TEXT                Output CSV file.
```

### Count all MLflow objects

Source: [count_objects.py](count_objects.py).

**Example**

```
count-objects --csv-file experiments.csv
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
  --versions-by-models  Model versions (by models count)
  --mlflow-api TEXT     MLflowApi implementation: iterator|search|both.
                        'search' directly calls MlflowClient.search methods.
                        'iterator' calls wrapper with page token. 'both'
                        compares the two.  [default: iterator]
```

## Dump objects 

### Dump run

Dumps run details.
* Source: [dump_run.py](dump_run.py).
* Shows info, params, metrics and tags sub-objects of run.
* Recursively lists run artifacts up to the specified level.
  * Note: A large value for `artifact_max_level` may execute many API calls.

Samples:
* Open source MLflow
[run.json](../../samples/oss_mlflow/regular_python/run.json).
* Databricks MLflow 
  * Non-autolog: [run.json](../../samples/databricks_mlflow/runs/sklearn_wine/run.json).
  * Autolog: [run_autolog.json](../../samples/databricks_mlflow/runs/sklearn_wine/run_autolog.json).

**Example**

```
dump-run 
  --run-id 4af184e8527a4f4a8fc563386807acb2 \
  --artifact-max-level 5 
```
```
{
  "summary": {
    "params": 2,
    "metrics": 1,
    "tags": 25,
    "artifacts": {
      "artifact_max_level": 10,
      "num_artifacts": 10,
      "num_bytes": 5158,
      "num_levels": 2
    }
  },
  "run": {
    "info": {
      "run_id": "0490018caf8044538d66048225a904c2",
      "run_uuid": "0490018caf8044538d66048225a904c2",
      "experiment_id": "1565792132797455",
      "run_name": "sklearn_onnx",
      "status": "FINISHED",
      "start_time": 1685336136094,
      "end_time": 1685336149565,
      "artifact_uri": "dbfs:/databricks/mlflow-tracking/1565792132797455/0490018caf8044538d66048225a904c2/artifacts",
      "lifecycle_stage": "active",
      "_start_time": "2023-05-29 00:55:36",
      "_end_time": "2023-05-29 00:55:50",
      "_duration": 13.471,
      "_experiment_name": "/Users/andre@piolet-knot.com/experiments/Sklearn_Wine_ONNX_ws"
    },
    "data": {
      "metrics": [
        {
          "key": "rmse",
          "value": 0.7986004372118107,
          "timestamp": 1685336149503,
          "step": 0
        }
      ],
. . .

```

**Usage**

```
dump-run --help

Options:
  --run-id TEXT                  Run ID.  [required]
  --artifact-max-level INTEGER   Number of artifact levels to recurse for run
                                 artifacts.  [default: 1]
  --explode-json-string BOOLEAN  Explode JSON string fields as JSON map.
  --show-tags-as-dict BOOLEAN    Show MLflow tags as a dictionary instead of a
                                 list of key/value pairs.  [default: True]
  --show-system-info BOOLEAN     Show system info.  [default: False]
  --format TEXT                  Output format. One of: json|yaml.
  --output-file TEXT             Output file.
```

### Dump experiment 

Dumps experiment details including its runs (optional how much of run data is shown).
* Source: [dump_experiment.py](dump_experiment.py)
* Samples:
  * Open source MLflow: 
    [experiment.json](../../samples/oss_mlflow/experiments/experiment.json)
  * Databricks MLflow: 
    [sklearn_wine_quality.json](../../samples/databricks_mlflow/experiments/sklearn_wine_quality.json) \-
    [sklearn_wine_quality_autolog.json](../../samples/databricks_mlflow/experiments/sklearn_wine_quality_autolog.json)
  
**Example**
```
dump-experiment \
  --experiment-id-or-name 1812 \
  --artifact-max-level 3 \
  --dump-runs True \
  --dump-run-data True
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
  --experiment-id-or-name TXT   Experiment ID or name  [required]
  --dump-runs BOOLEAN            Show runs  [default: False]
  --dump-run-data BOOLEAN        Show run data run if showing runs  [default:
                                 False] 
  --artifact-max-level INTEGER   Number of artifact levels to recurse for run
                                 artifacts.  [default: 1]
  --dump-permissions BOOLEAN     Dump Databricks permissions.  [default:
                                 False]
  --explode-json-string BOOLEAN  Explode JSON string fields as JSON map.
                                 [default: True]
  --show-tags-as-dict BOOLEAN    Show MLflow tags as a dictionary instead of a
                                 list of key/value pairs.  [default: True]
  --show-system-info BOOLEAN     Show system info.  [default: False]
  --format TEXT                  Output format. One of: json|yaml.  [default:
                                 json]
  --output-file TEXT             Output file.
```

### Dump experiment runs to CSV file - XX?

Create a CSV file of an experiment's runs from call to [mlflow.search_runs](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.search_runs). If argument `csv-file` is not specified the output file name will be `experiment_{EXPERIMENT_ID}.csv`.
```
python -m mlflow_tools.tools.dump_experiment_as_csv \
  --experiment-id-or-name sklearn \
  --csv-file sklearn.csv
```

### Dump registered model

Dumps a registered model, its versions  and optionally the run details of the versions.
* Source code: [dump_model.py](dump_model.py).
* JSON dump samples:
  * Open source MLflow: [registered_model.json](../../samples/oss_mlflow/models/registered_model.json)
  * Databricks MLflow: [registered_model.json](../../samples/databricks_mlflow/models/registered_model.json)

**Example**
```
dump-registered-model \
  --model sklearn_wine \
  --dump-runs True \
  --artifact-max-level
```
```
{
  "registered_model": {
    "name": "sklearn_wine_onnx",
    "creation_timestamp": 1684983781596,
    "last_updated_timestamp": 1685537065924,
    "description": "Skearn Wine Quality model",
    "aliases": [
      {
        "alias": "good-to-go_onnx",
        "version": "5"
      },
    ],
    "latest_versions": [
      {
        "name": "sklearn_wine_onnx",
        "version": "5",
        "creation_timestamp": 1685274127510,
        "last_updated_timestamp": 1685274127544,
        "_creation_timestamp": "2023-05-28 11:42:08",
        "_last_updated_timestamp": "2023-05-28 11:42:08",
        "current_stage": "Production",
        "description": "v5 Production - wine",
        "source": "/opt/mlflow/server/mlruns/1/6891e9c93f5b4c18a54c534e01c19378/artifacts/onnx-model",
        "run_id": "6891e9c93f5b4c18a54c534e01c19378",
        "status": "READY",
        "tags": {
          "registered_version_info": "v5 Production - wine"
        },
        "run_link": "",
        "_download_uri": {
          "artifact_uri": "/opt/mlflow/server/mlruns/1/6891e9c93f5b4c18a54c534e01c19378/artifacts/onnx-model"
        }
      }
    ],
    "_tracking_uri": "http://localhost:5020"
  },
. . .
  "version_runs": [ 
    { 
      "version": "5",
      "run": {
        "summary": {
          "params": 2,
        },
        "run": {
          "info": {
            "run_uuid": "6891e9c93f5b4c18a54c534e01c19378",
    { 
  ],
. . .
```

**Usage**
```
dump-model --help

Options:
  --model TEXT                   Registered model name.  [required]
  --dump-all-versions BOOLEAN    Dump all versions instead of latest versions.
                                 [default: False]
  --dump-runs BOOLEAN            Dump a version's run details.  [default:
                                 False]
  --artifact-max-level INTEGER   Number of artifact levels to recurse.
                                 [default: 0]
  --show-permissions BOOLEAN     Show Databricks permissions.  [default:
                                 False]
  --show-tags-as-dict BOOLEAN    Show MLflow tags as a dictionary instead of a
                                 list of key/value pairs.  [default: False]
  --explode-json-string BOOLEAN  Explode JSON string.  [default: False]
  --format TEXT                  Output format: json|yaml.
  --output-file TEXT             Output file
```

XXXX

### Dump model version

Dumps a registered model version optionally with all the MLflow objects connected to it - registered model, run and experiment.
* Databricks sample: [model_version.json](../../samples/databricks_mlflow/versions/model_version.json).
* Source code: [dump_model_version.py](dump_model_version.py).

**Example**
```
dump-model-version \
  --model sklearn_wine \
  --version 1 \
  --dump-run-model True \
  --dump-run True \
  --artifact-max-level 1 \
  --dump-experiment True \
  --dump-registered-model True \
  --dump-permissions True 
```

**Usage**
```
Options:
  --model TEXT                    Registered model name.  [required]
  --version TEXT                  Registered model version.  [required]
  --dump-run-model BOOLEAN        Dump the run model backing the version.
                                  [default: False]
  --dump-run BOOLEAN              Dump a version's run details.  [default:
                                  False]
  --artifact-max-level INTEGER    Number of artifact levels to recurse for run
                                  artifacts.  [default: 1]
  --dump-experiment BOOLEAN       Dump the run's experiment.  [default: False]
  --dump-registered-model BOOLEAN
                                  Dump a version's registered model (without
                                  version list details).  [default: False]
  --dump-permissions BOOLEAN      Dump Databricks permissions.  [default:
                                  False]
  --show-tags-as-dict BOOLEAN     Show MLflow tags as a dictionary instead of
                                  a list of key/value pairs.  [default: True]
  --explode-json-string BOOLEAN   Explode JSON string fields as JSON map.
                                  [default: True]
  --show-system-info BOOLEAN      Show system info.  [default: False]
  --format TEXT                   Output format. One of: json|yaml.  [default:
                                  json]
  --output-file TEXT              Output file.
```


## MISC

### List run or experiment tags

**Example**

```
list-run-tags \
  --object-id a32f905d3ad14f5b9495638a779e3bbd \
  --object-type run \
  --prefix mlflow \
  --max-tag-length 110
  --csv-file out.csv
```

```
Experiment: 1280664374380606  /Users/first.last@mycompany.com/experiments/Sklearn_Wine
Run ID: 851de1f466304650a77c949f5d386d9f
+--------------------------------------+--------------------------------------------------------------+
| key                                  | value                                                        |
|--------------------------------------+--------------------------------------------------------------|
| mlflow.databricks.cluster.id         | 0414-154233-qm0df4rx                                         |
| mlflow.databricks.cluster.info       | {"cluster_name":"ML_13.0","spark_version":"13.0.x-cpu-       |
| mlflow.databricks.cluster.libraries  | {"installable":[],"redacted":[]}                             |
| mlflow.databricks.notebook.commandID | 3527702579137640954_8374924253965797983_041de288996c42ef9716 |
| mlflow.databricks.notebookID         | 1280664374380381                                             |
| mlflow.databricks.notebookPath       | /Users/first.last@databricks.com/mlflow/mlflow-examples      |
| mlflow.databricks.notebookRevisionID | 1681630579984                                                |
| mlflow.databricks.webappURL          | https://mycompany.cloud.com                                  |
| mlflow.databricks.workspaceID        | 2556758628403379                                             |
| mlflow.databricks.workspaceURL       | https://mycompany.cloud.com                                  |
| mlflow.log-model.history             | [{"artifact_path":"model","flavors":{"python_function":{"pre |
| mlflow.runName                       | 851de1f466304650a77c949f5d386d9f                             |
| mlflow.source.name                   | /Users/first.last@mycompany.com/mlflow/mlflow-examples       |
| mlflow.source.type                   | NOTEBOOK                                                     |
| mlflow.user                          | first.last@mycompany.com                                     |
+--------------------------------------+--------------------------------------------------------------+
```

**Usage**
```
list-object-tags --help

Options:
  --run-id TEXT             Run ID  [required]
  --csv-file TEXT           Output CSV file
  --prefix TEXT             Show only tag keys starting with prefix
  --max-tag-length INTEGER  Show only first 'max-tag-length' characters of tag
                            value
```
