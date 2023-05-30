import mlflow
from mlflow_tools.display import dump_run
from mlflow_tools.display import dump_experiment
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


def test_dump_experiment():
    dump_experiment.dump(
        exp.name,
        dump_runs = True,
        dump_run_data = True
    )
