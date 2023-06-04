"""
Download the MLflow model(s) associated with a model URI.
You can download either:
  1. the run MLflow model 
  2. the registry MLflow model 
  2. or both
"""

import os
import shutil
import click
import mlflow
from mlflow.artifacts import download_artifacts
from mlflow_tools.common.model_download_utils import split_model_uri

client = mlflow.MlflowClient()


def _get_model_and_version(model_uri):
    model_name, version_or_stage = split_model_uri(model_uri)
    version = _get_version(model_name, version_or_stage)
    return model_name, version

def _get_version(model_name, version_or_stage):
    """ Get version number for a version_or_stage """
    if not version_or_stage.isdigit():
        versions = client.get_latest_versions(model_name, [version_or_stage])
        if len(versions) == 0:
            raise RuntimeError(f"No '{version_or_stage}' stage for model '{model_name}/{version_or_stage}'")
        version_or_stage = versions[0].version
    return version_or_stage

def _move_files(src_dir, dst_dir):
    for f in os.listdir(src_dir):
        shutil.move(os.path.join(src_dir,f), dst_dir)


def _download_registry_model(model_uri, output_dir, move_dir=True):
    reg_model_name, version = _get_model_and_version(model_uri)
    artifact_uri = client.get_model_version_download_uri(reg_model_name, version)
    from mlflow.utils.file_utils import TempDir
    with TempDir() as tmp:
        download_artifacts(artifact_uri, dst_path = tmp.path())
        files = os.listdir(tmp.path())
        if move_dir:
            _move_files(tmp.path(), output_dir)
            src_model_dir = os.path.join(output_dir, files[0])
            os.rename(src_model_dir, os.path.join(output_dir,"registry_model"))
        else:
            src_model_dir = os.path.join(tmp.path(), files[0])
            _move_files(src_model_dir, output_dir)


def download(model_uri, output_dir, which_model):
    if not model_uri.startswith("models:/"):
        raise RuntimeError(f"Model URI '{model_uri}' must start with 'models:'")
    if which_model == "run":
        download_artifacts(model_uri, dst_path=output_dir)

    elif which_model == "registry":
        _download_registry_model(model_uri, output_dir, move_dir=False)

    elif which_model == "both":
        download_artifacts(model_uri, dst_path=os.path.join(output_dir, "run_model"))
        _download_registry_model(model_uri, output_dir, move_dir=True)

    else:
        raise RuntimeError(f"Download which_model '{which_model}' must be one of: run|registry|both")


@click.command()
@click.option("--model-uri",
    help="Model URI of 'models:' scheme such as as 'models:/production'",
    type=str,
    required=True
)
@click.option("--output-dir",
    help="Output directory for downloaded model.",
    type=str,
    required=True
)
@click.option("--which-model",
    help="Which model: run|registry|both",
    type=str,
    default="run",
    show_default=True
)

def main(model_uri, output_dir, which_model):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    download(model_uri, output_dir, which_model)


if __name__ == "__main__":
    main()
