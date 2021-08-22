import os
import mlflow

def dump_mlflow_info():
    """ Show basic MLflow information. """
    print("MLflow Info:")
    print("  MLflow Version:", mlflow.version.VERSION)
    print("  Tracking URI:", mlflow.tracking.get_tracking_uri())
    mlflow_host = get_mlflow_host()
    print("  Real MLflow host:", mlflow_host)
    print("  MLFLOW_TRACKING_URI:", os.environ.get("MLFLOW_TRACKING_URI",""))
    print("  DATABRICKS_HOST:", os.environ.get("DATABRICKS_HOST",""))
    print("  DATABRICKS_TOKEN:", os.environ.get("DATABRICKS_TOKEN",""))

def get_mlflow_host():
    """ Returns the host (tracking URI) and token."""
    return get_mlflow_host_token()[0]

def get_mlflow_host_token():
    """ Returns the host (tracking URI) and token. """
    uri = os.environ.get('MLFLOW_TRACKING_URI',None)
    if uri is not None and uri != "databricks":
        return (uri,None)
    try:
        from mlflow_tools.common import databricks_cli_utils
        profile = os.environ.get('MLFLOW_PROFILE',None)
        #host_token = databricks_cli_utils.get_host_token(profile)
        return databricks_cli_utils.get_host_token(profile)
    #except databricks_cli.utils.InvalidConfigurationError as e:
    except Exception as e:
        print("WARNING:",e)
        return (None,None)

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
        except Exception:
            raise Exception(f"Cannot find experiment ID or name '{exp_id_or_name}'. Client: {client}'")
    return exp
