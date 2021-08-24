# Basic MLflow Tools 

## Overview

Some useful tools for MLflow. Run the examples from the root of repository.
* [List all experiments](#List-all-experiments)
* [Dump experiment or run as text](#Dump-experiment-or-run-as-text)
* [Dump experiment runs to CSV file](#Dump-experiment-runs-to-CSV-file)
* [Find best run of experiment](#Find-best-run-of-experiment)
* [Dump registered model as JSON or YAML](#Dump-registered-model-as-JSON-or-YAML)
* [Find matching artifacts](#Find-matching-artifacts)
* [Download model artifacts](#Download-model-artifacts)

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

## Dump experiment or run as text
Dumps all experiment or run information recursively.

### Overview
* [dump_experiment.py](dump_experiment.py) - Dumps experiment information.
  * If `showInfo` is true, then just the run infos will be dumped.
  * If `showData` is true, then an API call for each run will be executed. Beware of experiments with many runs.
* [dump_run.py](dump_run.py) - Dumps run information.
  * Shows info, params, metrics and tags.
  * Recursively shows all artifacts up to the specified level.
* A large value for `artifact_max_level` will execute many API calls.

### Run dump tools
```
python -m mlflow_tools.tools.dump_run --run_id 2cbab69842e4412c99bfb5e15344bc42 --artifact_max_level 5 
```
  
```
python -m mlflow_tools.tools.dump_experiment --experiment_id 1812 --show_info --show_data  --artifact_max_level 5
```

**Sample output for dump_experiment.py**
```
MLflow Version: 1.10.0
Experiment Details:
  experiment_id: 2
  name: sklearn
  artifact_location: /opt/mlflow/server/mlruns/1812/2
  lifecycle_stage: active
  tags: {}
  #runs: 3
Runs:
  Run 1/3:
    RunInfo:
      experiment_name: sklearn
      artifact_uri: /opt/mlflow/server/mlruns/1812/2/19323fe0d6fd400aa32c8fc923f0d7c8/artifacts
      experiment_id: 2
      lifecycle_stage: active
      run_id: 19323fe0d6fd400aa32c8fc923f0d7c8
      status: FINISHED
      user_id: andre
      start_time: 2020-07-30_03:35:14   1596080114006
      end_time:   2020-07-30_03:35:14   1596080114880
      _duration:  0.874 seconds
    Params:
      max_depth: 4
      max_leaf_nodes: 32
    Metrics:
      mae: 0.586355440756998
      r2: 0.2547711505595145
      rmse: 0.7640325255609308
    Tags:
      data_path: ../../data/train/wine-quality-white.csv
      mlflow.log-model.history: [{"run_id": "19323fe0d6fd400aa32c8fc923f0d7c8", "artifact_path": "sklearn-model", "utc_time_created": "2020-07-30 03:35:14.162889", "flavors": {"python_function": {"model_path": "model.pkl", "loader_module": "mlflow.sklearn", "python_version": "3.7.6", "env": "conda.yaml"}, "sklearn": {"pickled_model": "model.pkl", "sklearn_version": "0.20.2", "serialization_format": "cloudpickle"}}}, {"run_id": "19323fe0d6fd400aa32c8fc923f0d7c8", "artifact_path": "onnx-model", "utc_time_created": "2020-07-30 03:35:14.593898", "flavors": {"python_function": {"loader_module": "mlflow.onnx", "python_version": "3.7.6", "data": "model.onnx", "env": "conda.yaml"}, "onnx": {"onnx_version": "1.7.0", "data": "model.onnx"}}}]
      mlflow.runName: train.sh
      mlflow.source.git.commit: e7f840a012c019c65a688e4ba69fbb949371f3e1
      mlflow.source.name: main.py
      mlflow.source.type: LOCAL
      mlflow.user: andre
      run_origin: train.sh
      version.mlflow: 1.10.0
      version.python: 3.7.6
    Artifacts:
      Artifact 1/2 - level 0:
        path: plot.png
        bytes: 32417
      Artifact 2/2 - level 0:
        path: sklearn-model
        Artifact 1/3 - level 1:
          path: sklearn-model/MLmodel
          bytes: 357
        Artifact 2/3 - level 1:
          path: sklearn-model/conda.yaml
          bytes: 150
        Artifact 3/3 - level 1:
          path: sklearn-model/model.pkl
          bytes: 4893
    Total: bytes: 41050 artifacts: 7
```

## Dump experiment runs to CSV file

Create a CSV file of an experiment's runs from call to [mlflow.search_runs](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.search_runs). If argument `csv_file` is not specified the output file name will be `experiment_{EXPERIMENT_ID}.csv`.
```
python -m dump_experiment_as_csv --csv_file sklearn.csv
```

## Find best run of experiment

Find the best run for a metric of an experiment. 
Default order is descending (max). See [best_run.py](best_run.py).

Displays the run ID and best metric value.

```
python -m mlflow_tools.tools.best_run --experiment_id 2 --metric rmse --ascending 
```
```
Best run:
  run_id: 7890e3ec549442ebae453394ea7dd1ea
  rmse: 0.8829449794492825

```

## Dump registered model as JSON or YAML

Dumps a registered model and optionally the run details of each of its versions.
See [dump_model.py](dump_model.py).

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

## Find matching artifacts

Return artifact paths that match specified target filename.

**Example**

```
python -m mlflow_tools.tools.find_artifacts \
  --run-id 2cbab69842e4412c99bfb5e15344bc42 \
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
  --max-level INTEGER  Number of artifact levels to recurse.  [default:
                       9223372036854775807]
```

## Download model artifacts

Download the model artifacts associated with a model URI.

```
python -m mlflow_tools.tools.download_model \
   --model-uri models:/sklearn_wine
   --output-dir /tmp/my-model
```

```
python -m mlflow_tools.tools.download_model \
   --model-uri runs:/18f6b9a2f72f44de8bb9591d163c6754/sklearn-model \
   --output-dir /tmp/my-model
```

/tmp/my-model
```
+-sklearn-model/
  +-requirements.txt
  +-model.pkl
  +-conda.yaml
  +-MLmodel
```
