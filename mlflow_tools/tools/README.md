# Basic MLflow Tools 

## Overview

Some useful tools for MLflow. 

**Experiments**
* [Delete experiment](#Delete-experiment)

**Registered models**
* [Register run model as a registered model version with optional stage](#Register-run-model-as-a-registered-model-version-with-optional-stage)
* [Delete registered model](#Delete-registered-model)
* [Delete model stages](#Delete-model-stages)
* [Rename registered model](#Rename-registered-model)

**Other tools**
* [Find best run of experiment](#Find-best-run-of-experiment)
* [Find model artifact paths of a run](#Find-model-artifact-paths-of-a-run)
* [Find matching artifacts](#Find-matching-artifacts)
* [Download model artifacts](#Download-model-artifacts)
* [Call MLflow model server](#Call-MLflow-model-server)
* [Call http_client either MLflow API or Databricks API](#Call-http_client-either-MLflow-API-or-Databricks-API)

## Setup
```
export MLFLOW_TRACKING_URI=http://localhost:5000
```


## Experiments

### Delete experiment

Deletes an experiment or just its runs (and not the experiment).

```
delete-experiment \
  --experiment-id-or-name sklearn_wine
```

```
delete-experiment \
  --experiment-id-or-name sklearn_wine \
  --delete-only-runs True
```

**Usage**
```
delete-experiment --help

Options:
  --experiment-id-or-name TEXT  Experiment ID or name  [required]
  --delete-only-runs BOOLEAN    Delete only runs and not the experiment
                                [default: False]
```

## Registered models 


### Register run model as a registered model version with optional stage

```
register-model \
  --registered-model my-registered-model \
  --run-id 123 \
  --model-artifact my-model \
  --stage production
```

**Usage**
```
register-model --help

Options:
  --registered-model TEXT  New registered model name.  [required]
  --run-id TEXT            Run ID  [required]
  --model-artifact TEXT    Source relative model artifact path.  [required]
  --stage TEXT             Stage
```

### Delete registered model 
```
delete-model --model sklearn_wine
```

```
Deleting 3 versions for model 'Iris-Sklearn'
  Deleting: {'version': '3', 'stage': 'Production', 'status': 'READY', 'run_id': 'f444942453364b8985091c12ea7fa833'}
  Deleting: {'version': '2', 'stage': 'None', 'status': 'READY', 'run_id': 'g444942453364b8985091c12ea7fa833'}
  Deleting: {'version': '1', 'stage': 'Staging', 'status': 'READY', 'run_id': 'f444942453364b8985091c12ea7fa833'}
Deleting model 'Iris-Sklearn'
```

**Usage**
```
delete-model --help

Options:
  --model TEXT                    Registered model name  [required]
  --delete-only-versions BOOLEAN  Delete only versions and not the registered
                                  model
```

### Delete model stages

Delete specified model stages.

```
delete-model-stages \
  --model sklearn_wine \
  --stages None,Archived
```

**Usage**

```
Options:
  --model TEXT   Registered model name  [required]
  --stages TEXT  Stages to delete (comma delimited). Default is all stages.
```

### Rename registered model 

```
rename-model \
  --model Sklearn_Wine \
  --new-model new_Sklearn_Wine
```

```
Renaming model 'Sklearn_Wine' to 'new_Sklearn_Wine'
Transitioning versions temporarily for model 'Sklearn_Wine' to 'Archived' stage in order to rename model
  {"version": 2, "stage": Archived}
  {"version": 1, "stage": Staging}
Transitioning versions for model 'new_Sklearn_Wine' back to original stage
  {"version": 2, "stage": Archived}
  {"version": 1, "stage": Staging}
```

**Usage**

```
rename-model --help

Options:
  --model TEXT                   Model name to rename  [required]
  --new-model TEXT               New model name  [required]
  --fudge-version-stage BOOLEAN  Fudge version stage: Transition stage to
                                 'Archived' before delete, and then restore
                                 original version stage for new model.
                                 [default: True]
```

## Other tools

### Find best run of experiment

Find the best run for a metric of an experiment. 
Default order is descending (max). 

See [best_run.py](best_run.py).

```
python -m mlflow_tools.tools.best_run \
  --experiment-id-or-nam 2 \
  --metric rmse \
  --ascending True
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


### Find model artifact paths of a run

See [find_run_model_names.py](find_run_model_names.py).

**Example**

Assume the following run artifacts.
```
-artifacts/
 +-onnx-model/
 | +-MLmodel
 | +-requirements.txt
 | +-python_env.yaml
 | +-model.onnx
 | +-conda.yaml
 |
 +-model/
   +-MLmodel
   +-requirements.txt
   +-python_env.yaml
   +-model.pkl
   +-conda.yaml
```

Python code
```
from mlflow_tools.tools import find_artifacts

matches = find_artifacts.find_run_model_names(run_id)
for m in matches:
   print(m)
```
```
model
onnx-model
```

Python command line
```
python -m mlflow_tools.tools.find_run_model_names \
  --run-id 4af184e8527a4f4a8fc563386807acb2 \
```

```
Matches:
  model
  onnx-model
```

**Usage**
```
python -m mlflow_tools.tools.find_run_model_names  --help

Options:
  --run-id TEXT        Run ID.  [required]
```

### Find matching artifacts

Return artifact paths that match specified target filename.

See [find_artifacts.py](find_artifacts.py).

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
