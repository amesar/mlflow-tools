# Basic MLflow Tools 

## Overview

Some useful tools for MLflow. Run the examples from the root of repository.
* List all experiments
* Dump experiment as text
* Dump run as text
* Dump experiment runs as CSV file
* Find best run of an experiment

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
  
python -m mlflow_tools.tools.dump_experiment --experiment_id 1812 --show_info --show_data  --artifact_max_level 5
```

**Sample output for dump_experiment.py**
```
Experiment Details:
  experiment_id: 1812
  name: sklearn_wine_elasticNet
  artifact_location: /opt/mlflow/server/mlruns/1812
  lifecycle_stage: active
  #runs: 5
Runs:
  Run 0/5:
    RunInfo:
      run_uuid: fdc33f23d2ac4b0bae5f8181700c00ed
      experiment_id: 1812
      name: 
      source_type: 4
      source_name: train.py
      entry_point_name: 
      user_id: andre
      status: 3
      source_version: 47e8ec307671203cf5607ac2534cbd8fe5e05677
      lifecycle_stage: active
      artifact_uri: /opt/mlflow/server/mlruns/1812/fdc33f23d2ac4b0bae5f8181700c00ed/artifacts
      start_time: 2019-06-04_19:59:30   1559678370412
      end_time:   2019-06-04_19:59:32   1559678372819
      _duration:  2.407 seconds
    Params:
      l1_ratio: 0.5
      alpha: 0.001
    Metrics:
      mae: 0.5837497243928481  - timestamp: 1559678372 1970-01-19 01:14:38
      r2: 0.2726475054853086  - timestamp: 1559678372 1970-01-19 01:14:38
      rmse: 0.7504340478812797  - timestamp: 1559678372 1970-01-19 01:14:38
    Tags:
      data_path: ../../data/wine-quality/wine-quality-white.csv
      mlflow.source.git.commit: 47e8ec307671203cf5607ac2534cbd8fe5e05677
      platform: Darwin
      mlflow.source.name: train.py
      mlflow.source.type: LOCAL
    Artifacts:
      Artifact 1/5 - level 1:
        path: sklearn-model
        is_dir: True
        bytes: None
        Artifact 1/3 - level 2:
          path: sklearn-model/MLmodel
          is_dir: False
          bytes: 351
        Artifact 2/3 - level 2:
          path: sklearn-model/conda.yaml
          is_dir: False
          bytes: 119
        Artifact 3/3 - level 2:
          path: sklearn-model/model.pkl
          is_dir: False
          bytes: 627
      Artifact 2/5 - level 1:
        path: wine_ElasticNet-paths.png
        is_dir: False
        bytes: 27772
```

## Dump Experiment Runs to CSV file

Create a CSV file of an experiment's runs from call to [mlflow.search_runs](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.search_runs). If argument `csv_file` is not specified the output file name will be `experiment_{EXPERIMENT_ID}.csv`.
```
python -m dump_experiment_as_csv --csv_file sklearn.csv
```

## Find best run for experiment

Find the best run for a metric of an experiment. 
Default order is descending (max).

Displays the run ID and best metric value.

```
python -m mlflow_tools.tools.best_run  --experiment_id 2 --metric=rmse  --ascending 
```
```
Best run:
  run_id: 7890e3ec549442ebae453394ea7dd1ea
  rmse: 0.8829449794492825

```
