"""
Checks if model version runs exist
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
    local_utils.dump(version, "Version")
    comparison = check_version(version, download_dir)
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
    local_utils.dump(vr)
    dst_path = os.path.join(download_dir, "run_model")

    local_path1 = mlflow.artifacts.download_artifacts(
        artifact_uri = vr.source,
        dst_path = dst_path,
        tracking_uri = client._tracking_client.tracking_uri
    )
    print(">> CHECK.1: run_model_local_path:",local_path1)

    dst_path = os.path.join(download_dir, "reg_model")
    local_path2 = mlflow.artifacts.download_artifacts(
        artifact_uri = download_uri,
        dst_path = dst_path,
        tracking_uri = client._tracking_client.tracking_uri
    )
    print(">> CHECK.2: run_model_local_path:",local_path2)

    compare = local_utils.compare_paths_with_hash(local_path1, local_path2)
    print(">> CHECK.3a: EQUALS:",compare)
    #print(">> CHECK.3b: EQUALS:",compare[0])
    #local_utils.dump(compare,"CHECK.3")

    dct = {
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
    local_utils.dump(dct,"FINAL.k")

    return dct



@click.command()
@click.option("--model",
    help="Registered model",
    type=str,
    required=True
)
@opt_download_dir 
@click.option("--version-or-stage",
    help="Version or stage",
    type=str,
    required=True
)
@opt_report_file

def main(model, version_or_stage, download_dir, report_file):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    check_model(model, version_or_stage, download_dir, report_file)
    
if __name__ == "__main__":
    main()
