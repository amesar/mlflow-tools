"""
Model download utilities.

Nomenclature:
- Model URI - A URI with any of MLflow schemes - models, runs, s3, wasb.
- Models URI - models:/my-model/production.
- Runs URI - runs:/2079b9ee113b4b6c8ae631790d4c1009/sklearn-model.
- See: https://mlflow.org/docs/latest/tracking.html#artifact-stores.
"""

import mlflow
client = mlflow.MlflowClient()
#print("MLflow Version:", mlflow.__version__)
#print("MLflow Tracking URI:", mlflow.get_tracking_uri())


def download_model(model_uri, output_dir):
    """
    Downloads the model associated with the model URI.
    - For model scheme, downloads the model associated with the stage/version.
    - For run scheme, downloads the model associated with the run ID and artifact.
    :param: model_uri - MLflow model URI.
    :param:output_dir - Output directory for downloaded model.
    :return: The local path to the downloaded model.
    """
    if model_uri.startswith("runs") or model_uri.startswith("models"):
        run_id, path = get_run_id_and_model_relative_path(model_uri)
        print("run_id:",run_id)
        artifact_path = client.download_artifacts(run_id, path, dst_path=output_dir)
    else:
        artifact_path = model_uri
    return artifact_path


def get_run_id_and_model_relative_path(model_uri):
    """
    Returns the run ID and relative model artifact path associated with model version from a model URI (either runs: or models: scheme)
    :param:model_uri: MLflow model URI.
    :param:output_dir: Output directory for downloaded model.
    :return:output_dir: Tuple of run ID and relative model artifact path
    """
    if model_uri.startswith("runs"):
        run_id, path = split_model_uri(model_uri)
        return run_id, path
    elif model_uri.startswith("models"):
        model_name, version_or_stage = split_model_uri(model_uri)
        print("model_name:",model_name)
        print("version_or_stage:",version_or_stage)

        if version_or_stage.isdigit():
            v = client.get_model_version(model_name, version_or_stage)
        else:
            versions = client.get_latest_versions(model_name, [version_or_stage])
            if len(versions) == 0:
                raise RuntimeError(f"No '{version_or_stage}' stage for model '{model_name}'")
            v = versions[0]
        print("versions.source:           ",v.source)
        model_version_download_uri = client.get_model_version_download_uri(model_name, v.version)
        print("model_version_download_uri:",model_version_download_uri)
        relative_path = get_relative_model_path(v.source, v.run_id)
        print("relative_path:",relative_path)
        return v.run_id, relative_path
    else:
        raise RuntimeError(f"Only accepts 'models:/' and 'runs:/' scheme. model_uri: {model_uri}")


def split_model_uri(model_uri):
    """
    Splits an MLflow model URI into two parts
      - For models scheme, returns the model name and stage or version, e.g models:/sklearn_wine/production
      - For runs scheme, returns the run ID relative model path, e.g runs:/2079b9ee113b4b6c8ae631790d4c1009/sklearn-model
    :param: Models URI.
    :return: Tuple of model name and stage/version or tuple of run ID and relative model path.
    """
    idx = model_uri.find("/")
    path = model_uri[idx+1:]
    idx = path.find("/")
    return path[:idx], path[idx+1:]


def get_relative_model_path(absolute_model_path, run_id):
    """
    Returns the relative model path from an absolute 'source' URI
    For example '/dbfs:/databricks/mlflow/3532228/2079b9ee113b4b6c8ae631790d4c1009/artifacts/sklearn-model' returns 'sklearn-model'.
    :param: absolute_model_path
    :param: run_id
    :return: relative model path
    """
    idx = absolute_model_path.find(run_id)
    relative_model_path = absolute_model_path[1+idx+len(run_id):]
    if relative_model_path.startswith("artifacts/"): # Bizarre - sometimes there is no 'artifacts' after run_id
        relative_model_path = relative_model_path.replace("artifacts/","")
    return relative_model_path
