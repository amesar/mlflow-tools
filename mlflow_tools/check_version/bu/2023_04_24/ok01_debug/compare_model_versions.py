"""
Compare two model versions (from different workspaces).
"""

import os
import click
import mlflow
from mlflow_tools.common import mlflow_utils, io_utils
from mlflow_tools.tools.check import local_utils

def compare_versions(cfg, download_dir, compare_run_models, compare_reg_models, 
        verbose=False
    ):
    local_utils.dump(cfg,"Config")
    if not compare_run_models and not compare_reg_models:
        print(f"WARNING: Nothing to compare: compare_run_models={compare_run_models} compare_reg_models={compare_reg_models}")
        return
    cfg1 = cfg["tracking_server_01"]
    cfg2 = cfg["tracking_server_02"]

    print(">>  mlflow.tracking_uri:",  mlflow.get_tracking_uri())
    client1 = mlflow.MlflowClient(cfg1["host"])
    client2 = mlflow.MlflowClient(cfg2["host"])
    print(f">> MlflowClient 1: {client1}")
    print(f">> MlflowClient 2: {client2}")
    print(">>  mlflow.tracking_uri:",  mlflow.get_tracking_uri())

    models1 = client1.search_registered_models()
    print(">> #models1:",len(models1))
    models2 = client2.search_registered_models()
    print(">> #models2:",len(models2))

    versions1 = client1.get_latest_versions(cfg1["model"],[cfg1["stage"]])
    vr1 = versions1[0]
    if verbose:
        local_utils.dump(vr1,"TrackingServer1 Version")
    versions2 = client2.get_latest_versions(cfg2["model"],[cfg2["stage"]])
    vr2 = versions2[0]
    if verbose:
        local_utils.dump(vr2,"TrackingServer2 Version")

    if compare_run_models:
        run_res = do_compare_run_models(client1, client2, vr1, vr2, cfg1, cfg2, download_dir)
        local_utils.dump(run_res, "Run_Model_Comparison")
    if compare_reg_models:
        reg_res = do_compare_reg_models(client1, client2, vr1, vr2, cfg1, cfg2, download_dir)
        local_utils.dump(reg_res, "Reg_Model_Comparison")

    if compare_run_models:
        print(f"Run models equal: {run_res['equals']}")
    if compare_reg_models:
        print(f"Reg models equal: {reg_res['equals']}")


# ==== Run Model

def do_compare_run_models(client1, client2, vr1, vr2, cfg1, cfg2, download_dir):
    print("==== compare_run_models:")
    path1 = download_artifact(client1, vr1.source, cfg1, download_dir, "run_model", 1)
    path2 = download_artifact(client2, vr2.source, cfg2, download_dir, "run_model", 2)
    return do_compare(path1, path2)
# XX

# ==== Reg Model

def do_compare_reg_models(client1, client2, vr1, vr2, cfg1, cfg2, download_dir):
    print("======= compare_reg_models:")
    def _get_uri(client, vr):
        return client.get_model_version_download_uri(vr.name, vr.version)
    path1 = download_artifact(client1, _get_uri(client1,vr1), cfg1, download_dir, "reg_model", 1)
    path2 = download_artifact(client2, _get_uri(client2,vr2), cfg2, download_dir, "reg_model", 2)
    return do_compare(path1, path2)

# ==== Common

def do_compare(path1, path2):
    equals =  compare_paths(path1["local_path"], path2["local_path"])
    res = {
       "equals": equals,
       "tracking_server_01": path1,
       "tracking_server_02": path2
    }
    return res

# XX
# Use since client2 fails on mlflow.artifacts.download_artifacts
def download_artifact_run(client, vr, cfg, download_dir, model_type, idx):
    which = f"model{idx}"
    dst_path = os.path.join(download_dir, model_type, which)
    print(">> download_artifact_run: dst_path:",dst_path)
    os.makedirs(dst_path, exist_ok=True)
    download_uri = f"runs:/{vr.run_id}/model",
    download_uri = vr.source
    local_path = client.download_artifacts(
        vr.run_id, "model",
        dst_path = dst_path,
    )
    print(">> download_artifact.2: local_path:",local_path)
    local_path = adjust_path(local_path, cfg)
    dct = {
      "local_path": local_path,
      "download_uri": download_uri,
      "tracking_uri": client._tracking_client.tracking_uri
    }
    return dct

def download_artifact(client, download_uri, cfg, download_dir, model_type, idx):
    print(">> download_artifact: -----")
    print(">> download_artifact.1a: client:",client)
    print(">> download_artifact.1b: download_uri:",download_uri)
    which = f"model{idx}"
    dst_path = os.path.join(download_dir, model_type, which)

    local_path = mlflow_utils.download_artifacts(client, download_uri, dst_path)

    print(">> download_artifact.2: local_path:",local_path)
    local_path = adjust_path(local_path, cfg)
    dct = {
      "local_path": local_path,
      "download_uri": download_uri,
      "tracking_uri": client._tracking_client.tracking_uri
    }
    return dct

# ==== Common

def compare_paths(path1, path2):
    if os.path.isdir(path1):
        # MLmodel differs because of run ID
        compare = local_utils.compare_dirs(path1, path2)
        equals = compare["equals"]
        print(">> compare_paths: EQUALS dir:",equals)
    else:
        equals = local_utils.compare_files(path1, path2)
        print(">> compare_paths: EQUALS file:",equals)
    return equals


def adjust_path(path, cfg):
    return os.path.join(path, cfg.get("native_model",""))


# ==== Main

@click.command()
@click.option("--config-file",
    help="Configuration file",
    type=str,
    required=True
)
@click.option("--download-dir",
    help="Download directory for artifacts",
    type=str,
    required=True
)

@click.option("--compare-run-models", help="Compare run models", type=bool, is_flag=True)
@click.option("--compare-reg-models", help="Compare registered models", type=bool, is_flag=True)
@click.option("--verbose", help="Verbose", type=bool, is_flag=True)

def main(config_file, download_dir, compare_run_models, compare_reg_models, verbose):
    """ 
    Compare the MLflow models backing a registered model version. Two options:
    Args:
        aaa
        bbb
    """
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    cfg = io_utils.read_file(config_file)
    compare_versions(cfg, download_dir, compare_run_models, compare_reg_models, verbose)
    
if __name__ == "__main__":
    main()
