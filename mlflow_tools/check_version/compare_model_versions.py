"""
Compare two model versions: check that the cached registry models are the same and the run models are the same.
"""

import os
import click
import mlflow
from mlflow_tools.common import mlflow_utils, io_utils
from . import local_utils
from . click_options import opt_download_dir, opt_report_file

def compare_versions(cfg, download_dir, compare_run_models=True, compare_reg_models=True, report_file=None):
    local_utils.dump(cfg,"Config")
    if not compare_run_models and not compare_reg_models:
        print(f"WARNING: Nothing to compare: compare_run_models={compare_run_models} compare_reg_models={compare_reg_models}")
        return

    cfg1 = cfg["tracking_server_1"]
    client1 = mlflow.MlflowClient(cfg1["host"])
    vr1 = local_utils.get_version(client1, cfg1["model"], cfg1["version_or_stage"])
    vr1.download_uri = client1.get_model_version_download_uri(vr1.name, vr1.version)

    cfg2 = cfg["tracking_server_2"]
    client2 = mlflow.MlflowClient(cfg2["host"])
    vr2 = local_utils.get_version(client2, cfg2["model"], cfg2["version_or_stage"])
    vr2.download_uri = client2.get_model_version_download_uri(vr2.name, vr2.version)

    summary = {
        "tracking_server_1": {
            "client": client1._tracking_client.tracking_uri,
            "version": vr1.__dict__
        },
        "tracking_server_2": {
            "client": client2._tracking_client.tracking_uri,
            "version": vr2.__dict__
        },
    }
    local_utils.dump(summary,"Summary")
    report = {
       "System": local_utils.get_system_info(__file__),
       "Config": cfg,
       "Model_Version_Summary": summary
    }

    if compare_run_models:
        path1 = _download_artifact(client1, vr1.source, cfg1, download_dir, "run_model", 1)
        path2 = _download_artifact(client2, vr2.source, cfg2, download_dir, "run_model", 2)
        run_res = _compare_paths(path1, path2)
        report["Run_Model_Comparison"] = run_res
        local_utils.dump(run_res, "Run_Model_Comparison")
    if compare_reg_models:
        path1 = _download_artifact(client1, vr1.download_uri, cfg1, download_dir, "reg_model", 1)
        path2 = _download_artifact(client2, vr2.download_uri, cfg2, download_dir, "reg_model", 2)
        reg_res = _compare_paths(path1, path2)
        report["Reg_Model_Comparison"] = reg_res
        local_utils.dump(reg_res, "Reg_Model_Comparison")

    summary = {}
    if compare_run_models:
        summary["run_model"] = run_res["equals"]
    if compare_reg_models:
        summary["reg_model"] = reg_res["equals"]
    report["Comparison_Summary"] = summary 
    local_utils.dump(summary, "Comparison_Summary")
    if report_file:
        io_utils.write_file(report_file, report)

    return report


def _download_artifact(client, download_uri, cfg, download_dir, model_type, idx):
    which = f"server_{idx}"
    dst_path = os.path.join(download_dir, model_type, which)
    local_path = mlflow_utils.download_artifacts(client, download_uri, dst_path)
    local_path = _adjust_path(local_path, cfg)
    dct = {
      "tracking_uri": client._tracking_client.tracking_uri,
      "download_uri": download_uri,
      "local_path": local_path
    }
    return dct


def _compare_paths(path1, path2):
    res = local_utils.compare_paths_with_hash(path1["local_path"], path2["local_path"])
    return {
       "equals": res["equals"], 
       "tracking_server_1": res["path1"],
       "tracking_server_2": res["path2"]
    }


def _adjust_path(path, cfg):
    return os.path.join(path, cfg.get("native_model",""))


@click.command()
@click.option("--config-file",
    help="Configuration file",
    type=str,
    required=True
)
@opt_download_dir
@click.option("--compare-run-models", 
    help="Compare run models", 
    type=bool, 
    is_flag=True
)
@click.option("--compare-reg-models", 
    help="Compare registered models", 
    type=bool, 
    is_flag=True
)
@opt_report_file
def main(config_file, download_dir, compare_run_models, compare_reg_models, report_file):
    """ 
    Compare two model versions: check that the cached registry models are the same and the run models are the same.
    """
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    cfg = io_utils.read_file(config_file)
    compare_versions(cfg, download_dir, compare_run_models, compare_reg_models, report_file)

    
if __name__ == "__main__":
    main()
