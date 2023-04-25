"""
Checks if model version run model artifact matches the cached model registry model.
"""

import os
import click
import mlflow
from mlflow_tools.common import io_utils
from . import local_utils
from . click_options import opt_download_dir, opt_report_file

client = mlflow.MlflowClient()


def check_model(model_name, version_or_stage, download_dir, report_file=None):
    opts = { k:v for k,v in locals().items() }
    version = local_utils.get_version(client, model_name, version_or_stage)
    local_utils.dump(version.__dict__, "Version")
    comparison = check_version(version, download_dir)
    local_utils.dump(comparison,"Comparison")
    report = { 
        "System": local_utils.get_system_info(__file__),
        "Options": opts,
        "Version": version.__dict__,
        "Comparison": comparison
    }
    if report_file:
        io_utils.write_file(report_file, report)


def check_version(vr, download_dir):
    download_uri = client.get_model_version_download_uri(vr.name, vr.version)
    dst_path = os.path.join(download_dir, "run_model")

    local_path1 = mlflow.artifacts.download_artifacts(
        artifact_uri = vr.source,
        dst_path = dst_path,
        tracking_uri = client._tracking_client.tracking_uri
    )

    dst_path = os.path.join(download_dir, "reg_model")
    local_path2 = mlflow.artifacts.download_artifacts(
        artifact_uri = download_uri,
        dst_path = dst_path,
        tracking_uri = client._tracking_client.tracking_uri
    )

    compare = local_utils.compare_paths_with_hash(local_path1, local_path2)
    res = {
        "equals": compare["equals"],
        "run_model": {
            "download_uri": vr.source,
            "local_path": compare["path1"]
        },
        "reg_model": {
            "download_uri": download_uri,
            "local_path": compare["path2"]
        }
    }
    return res


@click.command()
@click.option("--model",
    help="Registered model name",
    type=str,
    required=True
)
@click.option("--version-or-stage",
    help="Model version or stage",
    type=str,
    required=True
)
@opt_download_dir 
@opt_report_file

def main(model, version_or_stage, download_dir, report_file):
    """
    Checks if model version run model artifact matches the cached model registry model.
    """
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    check_model(model, version_or_stage, download_dir, report_file)
    

if __name__ == "__main__":
    main()
