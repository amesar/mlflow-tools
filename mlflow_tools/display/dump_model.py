"""
Dump a registered model in JSON or YAML.
"""

import click
import mlflow

from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.common.timestamp_utils import fmt_ts_millis
from mlflow_tools.common import mlflow_utils
from mlflow_tools.common import permissions_utils
from mlflow_tools.common.click_options import (
    opt_artifact_max_level,
    opt_dump_permissions,
    opt_show_tags_as_dict,
    opt_explode_json_string,
    opt_show_system_info,
    opt_format,
    opt_output_file
)
from mlflow_tools.display.display_utils import dump_finish
from mlflow_tools.display import dump_run

http_client = MlflowHttpClient()


def _format_ts(dct, key):
    v = dct.get(key, None)
    if v: 
        dct[f"_{key}"] = fmt_ts_millis(int(v))


def _adjust_model_timestamps(model):
    model.pop("tags", None)
    latest_versions = model.pop("latest_versions", None)
    _format_ts(model, "creation_timestamp")
    _format_ts(model, "last_updated_timestamp")
    model["latest_versions"] = latest_versions


def _adjust_version_timestamps(versions):
    for vr in versions:
        uri = http_client.get("model-versions/get-download-uri", {"name": vr["name"], "version": vr["version"] })
        vr["_download_uri"] = uri
        _format_ts(vr, "creation_timestamp")
        _format_ts(vr, "last_updated_timestamp")


def _add_runs(versions, artifact_max_level, explode_json_string, show_tags_as_dict):
    runs = []
    for vr in versions:
        try:
            run = http_client.get(f"runs/get", { "run_id": vr['run_id'] })["run"]
            run = dump_run.build_run_extended(
                run = run,
                artifact_max_level = artifact_max_level,
                explode_json_string = explode_json_string,
                show_tags_as_dict = show_tags_as_dict
            )
            runs.append({ "version": vr["version"], "run": run })
        except MlflowToolsException:
            dct = { "model": vr["name"], "version": vr["version"], "run_id": vr["run_id"] }
            msg = f"WARNING: Run does not exist: {dct}"
            print(msg)
            runs.append({ "version": vr["version"], "run": msg })
    return runs


def dump(
        model_name,
        dump_all_versions = False,
        dump_runs = False,
        artifact_max_level = 0,
        explode_json_string  =  True,
        show_tags_as_dict = True,
        dump_permissions = False,
        show_system_info = False,
        format = "json",
        output_file = None,
        silent = False,
    ):

    model = mlflow_utils.get_registered_model(http_client, model_name, dump_permissions)
    _adjust_model_timestamps(model)
    model["_tracking_uri"] = mlflow.get_tracking_uri()
    if dump_all_versions:
        versions = http_client.get(f"model-versions/search", {"name": model_name})
        versions = versions["model_versions"]
        _adjust_version_timestamps(versions)
        del model["latest_versions"] 
        model["all_versions"] = versions
    else:
        versions =  model.get("latest_versions", None)
        _adjust_version_timestamps(versions)

    if dump_permissions and "id" in model: # if calling Databricks tracking server
        permissions_utils.add_model_permissions(model)

    dct = { "registered_model": model }
    if dump_runs:
        version_runs = _add_runs(versions, artifact_max_level, explode_json_string, show_tags_as_dict)
        dct["version_runs"] = version_runs

    dump_finish(dct, output_file, format, show_system_info, __file__, silent)

    return model


@click.command()
@click.option("--model",
     help="Registered model name.",
     type=str,
     required=True
)
@click.option("--dump-all-versions",
    help="Dump all versions instead of latest versions.",
    type=bool,
    default=False,
    show_default=True
)
@click.option("--dump-runs",
    help="Dump a version's run details.",
    type=bool,
    default=False,
    show_default=True
)
@opt_artifact_max_level
@opt_dump_permissions
@opt_show_tags_as_dict
@opt_explode_json_string
@opt_show_system_info
@opt_format
@opt_output_file

def main(model, 
       dump_all_versions, 
       dump_runs, 
       explode_json_string, 
       artifact_max_level, 
       show_tags_as_dict, 
       dump_permissions,
       show_system_info,
       format, 
       output_file,
    ):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    dump(
        model_name = model,
        dump_all_versions = dump_all_versions,
        dump_runs = dump_runs,
        explode_json_string = explode_json_string,
        artifact_max_level = artifact_max_level,
        show_tags_as_dict = show_tags_as_dict,
        dump_permissions = dump_permissions,
        show_system_info = show_system_info,
        format = format,
        output_file = output_file,
    )


if __name__ == "__main__":
    main()
