import os
import mlflow
from mlflow_tools.client import mlflow_auth_utils
from mlflow_tools.common import MlflowToolsException


def dump_mlflow_info():
    """ Show basic MLflow information. """
    print("MLflow Info:")
    print("  MLflow Version:", mlflow.version.VERSION)
    print("  Tracking URI:", mlflow.tracking.get_tracking_uri())
    mlflow_host = mlflow_auth_utils.get_mlflow_host()
    print("  Real MLflow host:", mlflow_host)
    print("  MLFLOW_TRACKING_URI:", os.environ.get("MLFLOW_TRACKING_URI",""))
    print("  DATABRICKS_HOST:", os.environ.get("DATABRICKS_HOST",""))
    print("  DATABRICKS_TOKEN:", os.environ.get("DATABRICKS_TOKEN",""))


def get_experiment(client, exp_id_or_name):
    """
    Gets an experiment either by ID or name.
    :param: client - MLflowClient.
    :param: exp_id_or_name - Experiment ID or name..
    :return: Experiment object.
    """
    exp = client.get_experiment_by_name(exp_id_or_name)
    if exp is None:
        try:
            exp = client.get_experiment(exp_id_or_name)
        except Exception as e:
            raise MlflowToolsException(f"Cannot find experiment ID or name '{exp_id_or_name}'. Client: {client}'. Ex: {e}")
    return exp


def get_last_run(mlflow_client, exp_id_or_name):
    exp = get_experiment(mlflow_client, exp_id_or_name)
    runs = mlflow_client.search_runs(exp.experiment_id, order_by=["attributes.start_time desc"], max_results=1)
    return runs[0]


def list_model_versions(client, model_name, get_latest_versions=False, stage=None):
    """ List 'all' or the 'latest' versions of registered model. """
    if get_latest_versions:
        versions = client.get_latest_versions(model_name)
    else:
        from mlflow_tools.common.iterators import SearchModelVersionsIterator
        versions = list(SearchModelVersionsIterator(client, filter=f"name='{model_name}'"))
    if stage:
        versions = [ vr for vr in versions if vr.current_stage.casefold() == stage.casefold() ]
    return versions


def calling_databricks():
    return mlflow.tracking.get_tracking_uri().startswith("databricks")


def mk_tags_dict(tags_array):
    return { x["key"]:x["value"] for x in tags_array }
