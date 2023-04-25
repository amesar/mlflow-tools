"""
Checks if model version runs exist
"""

import click

import os
import mlflow
from mlflow.exceptions import RestException, MlflowException
from mlflow_export_import.common.click_options import opt_export_latest_versions
from mlflow_export_import.common.timestamp_utils import fmt_ts_millis
from mlflow_export_import.common import utils, model_utils
from mlflow_export_import.bulk import bulk_utils 
from mlflow_export_import.tools import tools_utils

_logger = utils.getLogger(__name__)

client = mlflow.MlflowClient()

def check_model(model_name, stages, output_dir):
    print(">> model_name:",model_name)
    print(">> stages:",stages)

    #model = client.get_registered_model(model_name)
    #print(">> model:",model)

    versions = client.get_latest_versions(model_name, stages)
    print(">> version:",versions)
    for vr in versions:
        check_version(vr, output_dir)

def check_version(vr, output_dir):
    #print(">>   version:",vr)
    print(">>   version:")
    print(">>     version:",vr.version)
    print(">>     current_stage:",vr.current_stage)
    print(">>     run_id:",vr.run_id)
    print(">>     source:      ",vr.source)
    download_uri = client.get_model_version_download_uri(vr.name, vr.version)
    print(">>     download_uri:",download_uri)
    tools_utils.dump(vr)

    stage = vr.current_stage.lower()

    run = client.get_run(vr.run_id)
    dst_path = os.path.join(output_dir, f"{vr.version}_{stage}", "run_model")
    local_path1 = mlflow.artifacts.download_artifacts(
        artifact_uri = vr.source,
        dst_path = dst_path,
        tracking_uri = client._tracking_client.tracking_uri
    )
    print(">>     run_model_local_path:",local_path1)

    dst_path = os.path.join(output_dir, f"{vr.version}_{stage}", "reg_model")
    local_path2 = mlflow.artifacts.download_artifacts(
        artifact_uri = download_uri,
        dst_path = dst_path,
        tracking_uri = client._tracking_client.tracking_uri
    )
    print(">>     reg_model_local_path:",local_path2)
    compare = tools_utils.compare_dirs(local_path1, local_path2)
    print("> DIFF:",compare["equals"])
    #print("> DIFF:",compare)
    tools_utils.dump(compare)


@click.command()
@click.option("--model",
    help="Registered model",
    type=str,
    required=True
)
@click.option("--stages",
    help="Stages",
    type=None,
    required=False
)
@click.option("--output-dir",
    help="Output directory",
    type=str,
    required=True
)
def main(model, stages, output_dir):
    _logger.info("Options:")
    for k,v in locals().items():
        _logger.info(f"  {k}: {v}")
    if stages: 
        stages = stages.split(",")
    _logger.info(f"stages: {stages}")
    check_model(model, stages, output_dir)
    
if __name__ == "__main__":
    main()
