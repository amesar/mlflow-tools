# Export and Import Experiments, Runs or Registered Models

Tools to export and import MLflow runs, experiments or registered models from one tracking server to another.

## Overview

### Runs
  * Export a run to  a directory or zip file.
  * Import a run from a directory or zip file.
  * Copy a run from one tracking server to another.
  * Limitations
    * Nested runs are only supported when you import/copy an experiment. For a run, its a TODO.
    * Databricks does not support notebook revision imports.

### Experiments
  * Export an experiment and all its runs to a directory or zip file.
  * Import an experiment from a directory or zip file.
  * Copy an experiment from one tracking server to another.

### Registered Models
  * Export a registered model to a directory.
  * Import a registered model from a directory.


### Limitations
#### Databricks MLflow Tracking Server Notes for `Copy` tools
  * Copy tools do not work when both the source and destination trackings servers are Databricks MLflow.
  * Copy tools work for open source MLflow.
  * Things get more complicated for the `copy` feature when using a a Databricks tracking server, either as source or destination .
  * This is primarily because [MLflow client](https://github.com/mlflow/mlflow/blob/master/mlflow/tracking/client.py) constructor only accepts a tracking_uri. 
    * For open source MLflow this works fine and you can have the two clients (source and destination) in the same program.
    * For Databricks MLflow, the constructor is not used to initialize target servers. Environment variables are used to initialize the client, so only one client can exist.
  * To copy experiments when a Databricks server is involved, you have to use the more manual process of exporting and then importing the experiment.

### Common arguments 

`output` - Either a directory or zip file (if `output` has a zip extension).

`intput` - Either a directory or zip file (if `output` has a zip extension).

`notebook-formats` - If exporting a Databricks experiment, the run's notebook can be saved in the specified formats (comma-delimited argument). Each format is saved as `notebook.{format}`. Supported formats are  SOURCE, HTML, JUPYTER and DBC. See Databricks [Export Format](https://docs.databricks.com/dev-tools/api/latest/workspace.html#notebookexportformat) documentation.

`export-metadata-tags` - Creates metadata tags (starting with `mlflow_tools.metadata`) containing export information. Contains the source `mlflow` tags in addition to other information.
```
Name                                  Value
mlflow_tools.metadata.timestamp       1551037752
mlflow_tools.metadata.timestamp_nice  2019-02-24 19:49:12
mlflow_tools.metadata.experiment_id   2
mlflow_tools.metadata.experiment-name sklearn_wine
mlflow_tools.metadata.run-id          50fa90e751eb4b3f9ba9cef0efe8ea30
mlflow_tools.metadata.tracking_uri    http://localhost:5000
```

## Experiments

### Export experiment

Export an experiment to a directory or zip file.

**Arguments**

|Name | Required | Default | Description|
|-----|----------|---------|------------|
| experiment | yes | none | Source experiment name or ID |
| output | no | out | Destination directory or zip file |
| export-metadata-tags | no | False | Export source run metadata tags |
| notebook-formats | no | SOURCE | Databricks notebook formats. Values are SOURCE, HTML, JUPYTER, DBC |


#### Export example
```
python -u -m mlflow_tools.export_import.export_experiment --experiment=2 --output=out --export-metadata-tags=True
```
```
python -u -m mlflow_tools.export_import.export_experiment --experiment=sklearn_wine --output=exp.zip
```

#### Databricks export example

See the [Access the MLflow tracking server from outside Databricks](https://docs.databricks.com/applications/mlflow/access-hosted-tracking-server.html).
```
export MLFLOW_TRACKING_URI=databricks
export DATABRICKS_HOST=https://acme.cloud.databricks.com
export DATABRICKS_TOKEN=MY_TOKEN

python -u -m mlflow_tools.export_import.export_experiment --experiment=sklearn_wine --notebook-formats=DBC,SOURCE
```

#### Output 

Output export directory example
```
manifest.json
130bca8d75e54febb2bfa46875a03d59/
5a22839d66154001882e0632581fbf02/
```

manifest.json - source experiment information
```
{
  "experiment": {
    "experiment_id": "2",
    "name": "sklearn_wine",
    "artifact_location": "/opt/mlflow/server/mlruns/2",
    "lifecycle_stage": "active"
  },
  "export_info": {
    "export_time": "2019-07-21 13:36:28",
    "num_runs": 2
  },
  "run-ids": [
    "130bca8d75e54febb2bfa46875a03d59",
    "5a22839d66154001882e0632581fbf02"
  ],
  "failed_run-ids": []
}
```

### Import experiment

Import an experiment from a directory or zip file.

**Arguments**

|Name | Required | Default | Description|
|-----|----------|---------|------------|
| experiment-name | yes | none | Destination experiment name  - will be created if it does not exist |
| input | yes | | Source directory or zip file produced by export_experiment.py |
| use-src-user-id | no | False | Set the destination user ID to the source user ID. Source user ID is ignored when importing into Databricks since setting it is not allowed. |

**Run examples**

```
python -u -m mlflow_tools.export_import.import_experiment \
  --experiment-name=sklearn_wine \
  --input=out 
```
```
python -u -m mlflow_tools.export_import.import_experiment \
  --experiment-name=sklearn_wine \
  --input=exp.zip 
```

### Copy experiment from one tracking server to another

Copies an experiment from one MLflow tracking server to another.

Source: [copy_experiment.py](copy_experiment.py)

In this example we use:
* Source tracking server runs on port 5000 
* Destination tracking server runs on 5001

**Arguments**

|Name | Required | Default | Description|
|-----|----------|---------|------------|
| src-experiment | yes | none | Source experiment name or ID |
| dst-experiment-name | yes | none | Destination experiment name  - will be created if it does not exist |
| src-uri | yes | none | Source tracking server URI |
| dst-uri | yes | none |  Destination tracking server URI |
| use-src-user-id | no | False | Set the destination user ID to the source user ID. Source user ID is ignored when importing into Databricks since setting it is not allowed. |
| export-metadata-tags | no | False | Export mlflow_tools tags |
| import-metadata-tags | no | False | Import mlflow_tools tags |

**Run example**
```
python -u -m mlflow_tools.export_import. copy_experiment \
  --src-experiment=sklearn_wine \
  --dst-experiment-name=sklearn_wine_imported \
  --src-uri=http://localhost:5000 \
  --dst-uri=http://localhost:5001
```

## Runs

### Export run

Export run to directory or zip file.

**Arguments**

|Name | Required | Default | Description|
|-----|----------|---------|------------|
| run-id | yes | none | Source run ID |
| output | no | out | Destination directory or zip file |
| export-metadata-tags | no | False | Export source run metadata tags |

**Run examples**
```
python -u -m mlflow_tools.export_import.export_run \
  --run-id=50fa90e751eb4b3f9ba9cef0efe8ea30 \
  --output=out
  --export-metadata-tags=True
```
```
python -u -m mlflow_tools.export_import.export_run \
  --run-id=50fa90e751eb4b3f9ba9cef0efe8ea30 \
  --output=run.zip
```

Produces a directory with the following structure:
```
run.json
artifacts
  plot.png
  sklearn-model
    MLmodel
    conda.yaml
    model.pkl
```
Sample run.json
```
{   
  "info": {
    "run-id": "130bca8d75e54febb2bfa46875a03d59",
    "experiment_id": "2",
    ...
  },
  "params": {
    "max_depth": "16",
    "max_leaf_nodes": "32"
  },
  "metrics": {
    "mae": 0.5845562996214364,
    "r2": 0.28719674214710467,
  },
  "tags": {
    "mlflow.source.git.commit": "a42b9682074f4f07f1cb2cf26afedee96f357f83",
    "mlflow.runName": "demo.sh",
    "run_origin": "demo.sh",
    "mlflow.source.type": "LOCAL",
    "mlflow_tools.metadata.tracking_uri": "http://localhost:5000",
    "mlflow_tools.metadata.timestamp": 1563572639,
    "mlflow_tools.metadata.timestamp_nice": "2019-07-19 21:43:59",
    "mlflow_tools.metadata.run-id": "130bca8d75e54febb2bfa46875a03d59",
    "mlflow_tools.metadata.experiment_id": "2",
    "mlflow_tools.metadata.experiment-name": "sklearn_wine"
  }
}
```

### Import run

Imports a run from a directory or zip file.

**Arguments**

|Name | Required | Default | Description|
|-----|----------|---------|------------|
| experiment-name | yes | none | Destination experiment name  - will be created if it does not exist |
| input | yes | none | Source directory or zip file produced by export_run.py |
| use-src-user-id | no | False | Set the destination user ID to the source user ID. Source user ID is ignored when importing into Databricks since setting it is not allowed. |


**Run examples**
```
python -u -m mlflow_tools.export_import.import_run \
  --run-id=50fa90e751eb4b3f9ba9cef0efe8ea30 \
  --input=out \
  --experiment-name=sklearn_wine_imported
```

### Copy run from one tracking server to another

Copies a run from one MLflow tracking server to another.

Source: [copy_run.py](copy_run.py)

In this example we use
* Source tracking server runs on port 5000 
* Destination tracking server runs on 5001

**Arguments**

|Name | Required | Default | Description|
|-----|----------|---------|------------|
| src-run-id | yes | none | Source run ID |
| dst-experiment-name | yes | none | Destination experiment name  - will be created if it does not exist |
| src-uri | yes | none | Source tracking server URI |
| dst-uri | yes | none |  Destination tracking server URI |
| use-src-user-id | no | False | Set the destination user ID to the source user ID. Source user ID is ignored when importing into Databricks since setting it is not allowed. |
| export-metadata-tags | no | False | Export source run metadata tags |

**Run example**
```
export MLFLOW_TRACKING_URI=http://localhost:5000

python -u -m mlflow_tools.export_import.copy_run \
  --src-run-id=50fa90e751eb4b3f9ba9cef0efe8ea30 \
  --dst-experiment-name=sklearn_wine \
  --src-uri=http://localhost:5000 \
  --dst-uri=http://localhost:5001
```

## Registered Models

### Export registered model

Export a model to a directory.

Source: [export_model.py](export_model.py).

#### Arguments

|Name | Required | Default | Description|
|-----|----------|---------|------------|
| model | yes | none | Registered model name |
|  output-dir | no | out | Destination directory |

#### Run
```
python -u -m mlflow_tools.export_import.export_model --model=sklearn_wine --output-dir=out 
```

#### Output 

Output export directory example

```
+-749930c36dee49b8aeb45ee9cdfe1abb/
| +-artifacts/
|   +-plot.png
|   +-sklearn-model/
|   | +-model.pkl
|   | +-conda.yaml
|   | +-MLmodel
|   |  
+-model.json
```

model.json 
```
{
  "registered_model": {
    "name": "sklearn_wine",
    "creation_timestamp": "1587517284168",
    "last_updated_timestamp": "1587572072601",
    "description": "hi my desc",
    "latest_versions": [
      {
        "name": "sklearn_wine",
        "version": "1",
        "creation_timestamp": "1587517284216",
. . .
```

### Import registered model

Import a model from a directory.

Source: [import_model.py](import_model.py).

#### Arguments

|Name | Required | Default | Description|
|-----|----------|---------|------------|
| model | yes | none | Registered model name |
| experiment-name | yes | none | Destination experiment name  - will be created if it does not exist |
| input-dir | yes | none | Source directory or zip file produced by export_model.py |
| delete-model | no | False | First delete the model and all its versions |

#### Run

```
python -u -m mlflow_tools.export_import.import_model \
  --model=sklearn_wine \
  --experiment-name=sklearn_wine_imported \
  --input-dir=out  \
  --delete-model=True
```

```
Model to import:
  Name: sklearn_wine
  Description: my model
  2 latest versions
Deleting 1 versions for model 'sklearn_wine_imported'
  version=2 status=READY stage=Production run-id=f93d5e4d182e4f0aba5493a0fa8d9eb6
Importing latest versions:
  Version 1:
    current_stage: None:
    Run to import:
      run-id: 749930c36dee49b8aeb45ee9cdfe1abb
      artifact_uri: file:///opt/mlflow/server/mlruns/1/749930c36dee49b8aeb45ee9cdfe1abb/artifacts
      source:       file:///opt/mlflow/server/mlruns/1/749930c36dee49b8aeb45ee9cdfe1abb/artifacts/sklearn-model
      model_path: sklearn-model
      run-id: 749930c36dee49b8aeb45ee9cdfe1abb
    Importing run into experiment 'scratch' from 'out/749930c36dee49b8aeb45ee9cdfe1abb'
    Imported run:
      run-id: 03d0cfae60774ec99f949c42e1575532
      artifact_uri: file:///opt/mlflow/server/mlruns/13/03d0cfae60774ec99f949c42e1575532/artifacts
      source:       file:///opt/mlflow/server/mlruns/13/03d0cfae60774ec99f949c42e1575532/artifacts/sklearn-model
Version: id=1 status=READY state=None
Waited 0.01 seconds
```


### Dump all registered models

Calls the `registered-models/list` REST endpoint and produces `registered_models.json`.
```
python -u -m mlflow_tools.export_import.export_registered_models
```

```
cat registered_models.json

"registered_models_detailed": [
  {
    "registered_model": {
      "name": "sklearn_wine"
    },
    "creation_timestamp": "1571948394155",
    "last_updated_timestamp": "1571948394155"
    "latest_versions": [
      {
        "model_version": {
          "registered_model": {
            "name": "sklearn_wine"
          },
          "version": "2"
        },
  },
```
