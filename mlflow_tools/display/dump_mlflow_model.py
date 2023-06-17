"""
Dump MLflow model with ModelInfo  mlflow.models.get_model_info().
"""

import click
import mlflow
from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common import object_utils
from mlflow_tools.common.click_options import (
    opt_model_uri,
    opt_dump_run,
    opt_dump_experiment,
    opt_show_system_info,
    opt_output_file
)
from mlflow_tools.display.display_utils import dump_finish
from mlflow_tools.display import dump_run as _dump_run

http_client = MlflowHttpClient()


def build(model_uri, dump_run=False, dump_experiment=False, signature_details=False):
    model_info = mlflow.models.get_model_info(model_uri)
    dct = object_utils.obj_to_dict(model_info)
    _adjust_mlflow_model(dct, signature_details)
    dct = {
        "model_info": dct
    }
    if dump_run:
        run = _mk_run(model_info._run_id)
        run = run["run"]
        dct["run"] = run
        if dump_experiment:
            dct["experiment"] = _mk_experiment(run["info"]["experiment_id"])
    return dct


def dump(model_uri, dump_run=False, dump_experiment=False, signature_details=False, show_system_info=False, output_file=None):
    dct = build(model_uri, dump_run, dump_experiment, signature_details)
    dct = dump_finish(dct, output_file, "json", show_system_info, __file__)
    return dct


def _adjust_mlflow_model(dct, details=True):
    if details:
        dct.pop("_signature_dict", None)
        object_utils.scrub_dict(dct, bad_key="__objclass__")
    else:
        import json
        sig = dct.pop("_signature_dict", None)
        if dct.get("_signature"):
            dct["_signature"] = { 
                "inputs": json.loads(sig.get("inputs")),
                "outputs": json.loads(sig.get("outputs"))
            }


def _mk_run(run_id):
    artifact_max_level = 0
    rsp = http_client.get("runs/get", { "run_id": run_id })
    run = rsp["run"]
    return _dump_run.build_run_extended(
        run = run,
        artifact_max_level = artifact_max_level
    )


def _mk_experiment(experiment_id):
    from mlflow_tools.display.dump_experiment import adjust_experiment
    rsp = http_client.get("experiments/get", { "experiment_id": experiment_id })
    exp = rsp["experiment"]
    adjust_experiment(exp, show_tags_as_dict=True)
    return exp


@click.command()
@opt_model_uri
@click.option("--signature-details", 
    help="Signature details.", 
    type=bool, 
    default=False, 
    show_default=True
)
@opt_dump_run
@opt_dump_experiment
@opt_show_system_info
@opt_output_file

def main(model_uri, dump_run, dump_experiment, signature_details, show_system_info, output_file):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    dump(model_uri, dump_run, dump_experiment, signature_details, show_system_info, output_file)


if __name__ == "__main__":
    main()
