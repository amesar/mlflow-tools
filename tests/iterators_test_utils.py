
import mlflow
from mlflow.utils.mlflow_tags import MLFLOW_RUN_NOTE # NOTE: ""mlflow.note.content" - used for Experiment Description too!

# ====

def mk_test_object_name_default():
    return f"{TEST_OBJECT_PREFIX}_{mk_uuid()}"

TEST_OBJECT_PREFIX = "test_exim"

def now():
    import time
    return round(time.time())


def mk_uuid():
    import shortuuid
    return shortuuid.uuid()

# ====

def create_experiment(client, mk_test_object_name=mk_test_object_name_default):
    exp_name = f"{mk_test_object_name()}"
    mlflow.set_experiment(exp_name)
    exp = client.get_experiment_by_name(exp_name)
    client.set_experiment_tag(exp.experiment_id, "version_mlflow", mlflow.__version__)
    client.set_experiment_tag(exp.experiment_id, MLFLOW_RUN_NOTE, f"Description_{mk_uuid()}")
    exp = client.get_experiment(exp.experiment_id)
    for info in client.search_runs(exp.experiment_id):
        client.delete_run(info.run_id)
    return exp

# ====

def list_experiments(client):
    return [ exp for exp in client.search_experiments() if exp.name.startswith(TEST_OBJECT_PREFIX) ]

def delete_model(client, model_name):
    from mlflow_tools.common.iterators import SearchModelVersionsIterator
    versions = SearchModelVersionsIterator(client, filter=f"name='{model_name}'")
    print(f"Deleting model '{model_name}'")
    for vr in versions:
        if vr.current_stage == "None":
            client.delete_model_version(model_name, vr.version)
    client.delete_registered_model(model_name)


def delete_models(client):
    for model in client.search_registered_models(max_results=1000):
        delete_model(client, model.name)


def delete_experiments(client):
    for exp in client.search_experiments():
        client.delete_experiment(exp.experiment_id)
