import mlflow
from mlflow_tools.display import dump_run
from mlflow_tools.display import list_experiments
from . utils_test import create_experiment

exp = create_experiment()
with mlflow.start_run() as run:
    mlflow.log_metric("m1", 0.1)

run_id = run.info.run_id
artifact_max_level = 4


def test_dump_run_as_json():
    dump_run.dump(run_id, artifact_max_level, "json", True)


def test_dump_run_as_yaml():
    dump_run.dump(run_id, artifact_max_level, "yaml", True)


def test_dump_run_as_txt():
    dump_run.dump(run_id, artifact_max_level, "txt", True)


def test_list_experiments():
    path = "/tmp/experiments.csv" # TODO: make a tmpdir
    list_experiments.list(path)
