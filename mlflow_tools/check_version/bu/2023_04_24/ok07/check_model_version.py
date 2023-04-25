"""
Checks if model version runs exist
"""

import click

import os
import mlflow

#from mlflow_export_import.common import utils

from . import local_utils
#from mlflow_tools.tools.check import local_utils

#_logger = utils.getLogger(__name__)

client = mlflow.MlflowClient()

def check_model(model_name, version_or_stage, download_dir):
    print(">> model_name:",model_name)
    print(">> version_or_stage:",version_or_stage)
    vr = local_utils.get_version(client, model_name, version_or_stage)
    local_utils.dump(vr,"Version")
    check_version(vr, download_dir)

def check_version(vr, download_dir):
    download_uri = client.get_model_version_download_uri(vr.name, vr.version)
    local_utils.dump(vr)
    dst_path = os.path.join(download_dir, "run_model")

    local_path1 = mlflow.artifacts.download_artifacts(
        artifact_uri = vr.source,
        dst_path = dst_path,
        tracking_uri = client._tracking_client.tracking_uri
    )
    print(">>     run_model_local_path:",local_path1)

    dst_path = os.path.join(download_dir, "reg_model")
    local_path2 = mlflow.artifacts.download_artifacts(
        artifact_uri = download_uri,
        dst_path = dst_path,
        tracking_uri = client._tracking_client.tracking_uri
    )
    compare = local_utils.compare_dirs(local_path1, local_path2)
    print("> EQUALS:",compare["equals"])
    local_utils.dump(compare)


@click.command()
@click.option("--model",
    help="Registered model",
    type=str,
    required=True
)
@click.option("--version-or-stage",
    help="Version or stage",
    type=str,
    required=True
)
@click.option("--download-dir",
    help="Output directory",
    type=str,
    required=True
)
def main(model, version_or_stage, download_dir):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    check_model(model, version_or_stage, download_dir)
    
if __name__ == "__main__":
    main()
