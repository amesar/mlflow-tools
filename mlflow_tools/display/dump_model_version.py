"""
Dump a registered model version in JSON or YAML.
"""

import click
from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.common import model_download_utils
from mlflow_tools.common import io_utils, object_utils
from mlflow_tools.common.click_options import (
    opt_dump_raw,
    opt_artifact_max_level,
    opt_show_tags_as_dict,
    opt_explode_json_string,
    opt_dump_run,
    opt_dump_experiment,
    opt_dump_permissions,
    opt_show_system_info,
    opt_format,
    opt_output_file
)
from mlflow_tools.display import dump_run as _dump_run
from mlflow_tools.display import dump_registered_model as _dump_registered_model
from mlflow_tools.display import dump_experiment as _dump_experiment
from mlflow_tools.display import dump_mlflow_model as _dump_mlflow_model
from mlflow_tools.display.display_utils import build_artifacts
from mlflow_tools.display.display_utils import dump_finish
from mlflow_tools.display.display_utils import adjust_model_version

http_client = MlflowHttpClient()


def dump(
        model_name,
        version,
        dump_raw = False,
        dump_run = False,
        dump_model_info = False,
        dump_model_artifacts = False,
        dump_registered_model = False,
        dump_experiment = False,
        artifact_max_level = 1,
        show_tags_as_dict = True,
        explode_json_string = True,
        dump_permissions = False,
        show_system_info = False,
        format = "json",
        output_file = None,
        silent = False
    ):
    rsp = http_client.get("model-versions/get", { "name": model_name, "version": version })
    vr = rsp["model_version"]
    if dump_raw:
        if output_file:
            io_utils.write_file(output_file, vr)
        object_utils.dump_dict_as_json(vr)
        return vr

    adjust_model_version(http_client, vr, show_tags_as_dict)

    dct = {
      "model_version": vr
    }

    if dump_registered_model:
        reg_model = _dump_registered_model.dump(
            model_name,
            artifact_max_level = 0,
            explode_json_string  =  explode_json_string,
            show_tags_as_dict = show_tags_as_dict,
            dump_permissions = dump_permissions,
            silent = True
        )
        reg_model["latest_versions"] = len(reg_model["latest_versions"])
        dct["registered_model"] = reg_model

    if dump_model_info:
        dct["mlflow_model_infos"] = _mk_model_infos(vr)

    if dump_model_artifacts:
        dct["mlflow_model_artifacts"] = _mk_model_artifacts(vr, artifact_max_level)

    if dump_run or dump_experiment:
        _mk_run_and_experiment(dct, vr, dump_run, dump_experiment, dump_permissions, 
            explode_json_string, show_tags_as_dict, artifact_max_level, silent)

    dct = dump_finish(dct, output_file, format, show_system_info, __file__, silent=silent)

    return dct


def _mk_model_infos(vr):
    def _adjust(dct):
        """ move the '_model_uri' key to the beginning of dct for readability/clarity. """
        from collections import OrderedDict
        dct = OrderedDict(dct["model_info"])
        dct.move_to_end("_model_uri", last=False)
        return dct
    model_uri = f'models:/{vr["name"]}/{vr["version"]}'
    return {
        "model_info_run": _adjust(_dump_mlflow_model.build(model_uri)),
        "model_info_registry": _adjust(_dump_mlflow_model.build(vr["_download_uri"]))
    }


def _mk_model_artifacts(vr, artifact_max_level):
    try:
        rsp = http_client.get("runs/get", { "run_id": vr["run_id"] })
        run = rsp["run"]
        info = run["info"]
        path = model_download_utils.get_relative_model_path(vr["source"], info["run_id"])
        artifacts = build_artifacts(info["run_id"], path, artifact_max_level)
        return {
            "summary": artifacts.get("summary"),
            "artifacts": artifacts.get("files")
        }
    except MlflowToolsException as e:
        print(f"WARNING: {e}")
        return {
            "ERROR": str(e)
        }


def _mk_run_and_experiment(dct, vr, dump_run, dump_experiment, dump_permissions, 
        explode_json_string, show_tags_as_dict, artifact_max_level, silent
    ):
    try:
        if dump_run or dump_experiment:
            rsp = http_client.get("runs/get", { "run_id": vr["run_id"] })
            run = rsp["run"]
            dct["run"] = _dump_run.build_run_extended(
                run = run,
                artifact_max_level = artifact_max_level,
                explode_json_string = explode_json_string,
                show_tags_as_dict = show_tags_as_dict
            )
        if dump_experiment:
            exp = _dump_experiment.dump(run["info"]["experiment_id"],
                    dump_runs = False,
                    dump_permissions = dump_permissions,
                    explode_json_string = explode_json_string,
                    show_tags_as_dict = show_tags_as_dict,
                    silent = silent
            )
            dct["experiment"] = exp
    except MlflowToolsException as e:
        print(f"WARNING: {e}")
        dct["run"] = { "ERROR": str(e) }


@click.command()
@click.option("--model",
     help="Registered model name.",
     type=str,
     required=True
)
@click.option("--version",
     help="Registered model version.",
     type=str,
     required=True
)
@opt_dump_raw
@click.option("--dump-model-info",
    help="Dump the ModelInfo for both the run and registry MLflow model.",
    type=bool,
    default=False,
    show_default=True
)
@click.option("--dump-model-artifacts",
    help="Dump the run model artifacts.",
    type=bool,
    default=False,
    show_default=True
)
@opt_dump_run
@click.option("--dump-registered-model",
    help="Dump a version's registered model (without version list details).",
    type=bool,
    default=False,
    show_default=True
)
@opt_artifact_max_level
@opt_dump_experiment
@opt_dump_permissions
@opt_show_tags_as_dict
@opt_explode_json_string
@opt_show_system_info
@opt_format
@opt_output_file

def main(model, version, 
        dump_raw, 
        dump_run, 
        dump_model_info,
        dump_model_artifacts, 
        dump_experiment,
        dump_registered_model,
        artifact_max_level, show_tags_as_dict, explode_json_string,
        dump_permissions,
        show_system_info,
        format,
        output_file
    ):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    dump(model, version, 
        dump_raw, 
        dump_run, 
        dump_model_info,
        dump_model_artifacts, 
        dump_registered_model,
        dump_experiment,
        artifact_max_level, show_tags_as_dict, explode_json_string,
        dump_permissions,
        show_system_info,
        format,
        output_file
    )


if __name__ == "__main__":
    main()
