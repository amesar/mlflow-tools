import os
import mlflow
from  mlflow.exceptions import RestException
from mlflow_tools.client import mlflow_auth_utils
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.client.http_client import MlflowHttpClient


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
    :param: client - Union: MLflowClient or MlflowHttpClient.
    :param: exp_id_or_name - Experiment ID or name..
    :return: Experiment object or dict.
    """
    if isinstance(client, MlflowHttpClient):
        return get_experiment_http_client(client, exp_id_or_name)
    else:
        return get_experiment_mlflow_client(client, exp_id_or_name)


def get_experiment_mlflow_client(mlflow_client, exp_id_or_name):
    """
    Gets an experiment either by ID or name.
    :param: mlflow_client - MLflowClient.
    :param: exp_id_or_name - Experiment ID or name..
    :return: Experiment object.
    """
    exp = mlflow_client.get_experiment_by_name(exp_id_or_name)
    if exp is None:
        try:
            exp = mlflow_client.get_experiment(exp_id_or_name)
        except RestException as e:
            raise MlflowToolsException(f"Cannot find experiment ID or name '{exp_id_or_name}'. Client: {mlflow_client}'. Ex: {e}")
    return exp


def get_experiment_http_client(http_client, exp_id_or_name):
    """
    Gets an experiment either by ID or name.
    :param: http_client - MLflowClient.
    :param: exp_id_or_name - Experiment ID or name..
    :return: Experiment object.
    """
    try:
        exp = http_client.get("experiments/get-by-name", {"experiment_name": exp_id_or_name})
    except MlflowToolsException as e:
        try:
            exp = http_client.get("experiments/get", {"experiment_id": exp_id_or_name})
        except RestException as e:
            raise MlflowToolsException(f"Cannot find experiment ID or name '{exp_id_or_name}'. Client: {http_client}'. Ex: {e}")
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


def download_artifacts(client, download_uri, dst_path=None, fix=True):
    """
    Apparently the tracking_uri argument is not honored for mlflow.artifacts.download_artifacts().
    It seems that tracking_uri is ignored and the global mlflow.get_tracking_uri() is always used.
    If the two happen to be the same operation will succeed.
    If not, it fails.
    Issue: Merge pull request #104 from mingyu89/fix-download-artifacts
           https://github.com/mlflow/mlflow-export-import/pull/104
    """
    if fix:
        previous_tracking_uri = mlflow.get_tracking_uri()
        mlflow.set_tracking_uri(client._tracking_client.tracking_uri)
        local_path = mlflow.artifacts.download_artifacts(
            artifact_uri = download_uri,
            dst_path = dst_path,
        )
        mlflow.set_tracking_uri(previous_tracking_uri)
    else:
        local_path = mlflow.artifacts.download_artifacts(
            artifact_uri = download_uri,
            dst_path = dst_path,
            tracking_uri = client._tracking_client.tracking_uri
        )
    return local_path


def calling_databricks():
    return mlflow.tracking.get_tracking_uri().startswith("databricks")


def mk_tags_dict(tags_array):
    return { x["key"]:x["value"] for x in tags_array }
