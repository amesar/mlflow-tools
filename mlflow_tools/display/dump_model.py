"""
Dump a registered model in JSON or YAML.
"""

import click
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.common.timestamp_utils import fmt_ts_millis
from mlflow_tools.common import mlflow_utils
from mlflow_tools.common import permissions_utils
from mlflow_tools.common.click_options import opt_show_permissions, opt_show_tags_as_dict
from mlflow_tools.client.http_client import MlflowHttpClient
from . import dump_dct, dump_run, write_dct

client = MlflowHttpClient()


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
        _format_ts(vr, "creation_timestamp")
        _format_ts(vr, "last_updated_timestamp")


def _add_runs(versions, artifact_max_level, explode_json_string, show_tags_as_dict):
    runs = []
    for vr in versions:
        try:
            run = client.get(f"runs/get", { "run_id": vr['run_id'] })["run"]
            run = dump_run.build_run(
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
        format = "json", 
        dump_all_versions = False,
        dump_runs = False, 
        explode_json_string  =  False,
        artifact_max_level = 0,
        output_file = None,
        show_tags_as_dict = False,
        show_permissions = False
    ):

    if show_permissions and mlflow_utils.calling_databricks():
        model = client.get(f"databricks/registered-models/get", {"name": model_name} )
        model = model["registered_model_databricks"]
    else:
        model = client.get(f"registered-models/get", {"name": model_name} )
        model = model["registered_model"]
    _adjust_model_timestamps(model)
    if dump_all_versions:
        versions = client.get(f"model-versions/search", {"name": model_name})
        versions = versions["model_versions"]
        _adjust_version_timestamps(versions)
        del model["latest_versions"] 
        model["all_versions"] = versions
    else:
        versions =  model.get("latest_versions", None)
        _adjust_version_timestamps(versions)

    if show_permissions and mlflow_utils.calling_databricks():
        permissions_utils.add_model_permissions(model)

    if dump_runs:
        version_runs = _add_runs(versions, artifact_max_level, explode_json_string, show_tags_as_dict)
        model["_version_runs"] = version_runs

    dump_dct(model, format)

    if output_file and len(output_file) > 0:
        write_dct(model, output_file, format)

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
@click.option("--artifact-max-level",
    help="Number of artifact levels to recurse.",
    type=int,
    default=0,
    show_default=True
)
@opt_show_permissions
@opt_show_tags_as_dict
@click.option("--explode-json-string",
    help="Explode JSON string.",
    type=bool,
    default=False,
    show_default=True
)
@click.option("--format", 
    help="Output format: json|yaml.",
    type=str,
    default="json"
)
@click.option("--output-file", 
    help="Output file", 
    type=str,
    required=False,
    show_default=True
)

def main(model, dump_all_versions, dump_runs, explode_json_string, artifact_max_level, output_file, 
       format, show_tags_as_dict, show_permissions):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    dump(
        model_name = model, 
        format = format, 
        dump_all_versions = dump_all_versions, 
        dump_runs = dump_runs, 
        explode_json_string = explode_json_string, 
        artifact_max_level = artifact_max_level, 
        output_file = output_file, 
        show_tags_as_dict = show_tags_as_dict,
        show_permissions = show_permissions
    )


if __name__ == "__main__":
    main()
