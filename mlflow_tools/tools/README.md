# mlflow-tools - Tools 

## Overview

Some useful tools for MLflow.
* List all experiments
* Dump experiment or runs as text
  * Dump Run
  * Dump Experiment
* Dump experiment runs as CSV
* Find best run for an experiment
* Execute examples from root of repository.

## List all experiments
List all experiments. See [list_experiments.py](list_experiments.py).
```
python -m mlflow_tools.tools.list_experiments.py --csv_file my_experiments.csv
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
* [dump_run.py](dump_run.py) - Dumps run information.
  * Shows info, params, metrics and tags.
  * Recursively shows all artifacts up to the specified level.
* [dump_experiment.py](dump_experiment.py) - Dumps experiment information.
  * If `showInfo` is true, then just the run infos will be dumped.
  * If `showData` is true, then an API call for each run will be executed. Beware of experiments with many runs.
* A large value for `artifact_max_level` also incurs many API calls.

### Run dump tools
```
export PYTHONPATH=../..

python -m mlflow_tools.tools.dump_run.py --run_id 2cbab69842e4412c99bfb5e15344bc42 --artifact_max_level 5 
  
python -m mlflow_tools.tools.dump_experiment.py --experiment_id 1812 --show_info --show_data  --artifact_max_level 5
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

Create a flattened table of an experiment's runs and dump to CSV file.

All info, data.params, data.metrics and data.tags fields will be flattened into one table. In order to prevent name clashes, data fields will be prefixed with:
* \_p\_ - params
* \_m\_ - metrics
* \_t\_ - tags

Since run data (params, metrics, tags) fields are not required to be the same for each run, we build a sparse table. Note the blank values for `_m_rmse` and `_t_exp_id` in the csv_file sample below.

By default, all the run.data.* fields are displayed. The `skip_` options control which are displayed.

Options:
* experiment - Experiment ID or name
* sort - opinionated pretty sort:
  *  Order of columns: 
    * run.info
      *  First columns: run_id, start_time, end_time
      *  artifact_uri is last colum as it is very long
   * run.info.data.params
   * run.info.data.metrics
   * run.info.data.tags
* pretty_time - Human-readable timestamps
* duration - Display run duration (end_time-sgtart_time) as `__duration` field
* skip_params - Don't display params fields
* skip_metrics - Don't display metrics fields
* skip_tags - Don't display tags fields
* nan_to_blank - Convert Pandas NaN to ""
* csv_file - If not specified, the CSV file will be created from the experiment ID as in `exp_runs_2.csv`.

```
pythom -m runs_to_pandas_converter.py \
  --experiment 2 \
  --sort \
  --pretty_time \
  --duration \
  --skip_params \
  --skip_metrics \
  --skip_tags \
  --nan_to_blank \
  --csv_file output.csv

```

## Find best run for an experiment

You specify a metric for an experiment and find its best run. Default order is descending (max).

Returns the run ID and metric value.

```
python -m mlflow_tools.tools.best_run  --experiment_id 2 --metric=rmse  --ascending 
```
```
Best: ('5ac384a850dd4c078ad2a219cfc4f4ef', 0.747225794954636)
```
