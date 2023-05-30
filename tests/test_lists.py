import mlflow
from mlflow_tools.display import list_experiments
from . utils_test import create_experiment

exp = create_experiment()
with mlflow.start_run() as run:
    mlflow.log_metric("m1", 0.1)

def test_list_experiments():
    path = "/tmp/experiments.csv" # TODO: make a tmpdir
    list_experiments.list(path)
