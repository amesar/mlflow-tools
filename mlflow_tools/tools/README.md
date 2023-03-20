# Basic MLflow Tools 

## Overview

Some useful tools for MLflow. Run the examples from the root of repository.

**Registered models**
* [Register a run's model as a registered model version and optional stage](#Register-a-run's-model-as-a-registered-model-version-and-optional-stage)
* [Delete registered model](#Delete-registered-model)
* [Delete model stages](#Delete-model-stages)


**Other tools**
* [Find best run of experiment](#Find-best-run-of-experiment)
* [Find matching artifacts](#Find-matching-artifacts)
* [Download model artifacts](#Download-model-artifacts)
* [Call MLflow model server](#Call-MLflow-model-server)
* [Call http_client either MLflow API or Databricks API](#Call-http_client-either-MLflow-API-or-Databricks-API)

## Setup
```
export MLFLOW_TRACKING_URI=http://localhost:5000
```


## Registered models 


### Register a run's model as a registered model version and optional stage

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

### Delete registered model 
```
python -m mlflow_tools.tools.delete_model --model sklearn_wine
```
**Usage**
```
python -m mlflow_tools.tools.delete_model --help

Options:
  --model TEXT                    Registered model name  [required]
  --delete-only-versions BOOLEAN  Delete only versions and not the registered
                                  model
```

### Delete model stages

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

## Other tools

### Find best run of experiment

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


### Find matching artifacts

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

### Download model artifacts

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


### Call MLflow model server

Invoke the MLflow model server to score the wine quality file.

Invoke open source MLfow model server
```
python -m mlflow_tools.tools.call_model_server \
   --api-uri http://localhost:5001/invocations \
   --datapath wine-quality-split-orient.json
```

Invoke Databricks MLfow model server
```
python -m mlflow_tools.tools.call_model_server \
   --api-uri https://my-workspace.mycompany.com/model-endpoint/Sklearn_Train_Predict/1/invocations \
   --datapath wine-quality-split-orient.json \
   --token MY_TOKEN
```



### Call http_client - either MLflow API or Databricks API

**Usage**
```
python -m mlflow_tools.client.http_client --help

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
