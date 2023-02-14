"""
Dump a registered model in JSON or YAML.
"""

import click
import json
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.common.http_client import MlflowHttpClient
from mlflow_tools.common.timestamp_utils import fmt_ts_millis
from . import dump_dct, dump_run

client = MlflowHttpClient()


def _format_ts(dct, key):
    v = dct.get(key, None)
    if v: 
        dct[f"_{key}"] = fmt_ts_millis(int(v))


def dump_versions(versions, dump_runs, artifact_max_level, explode_json_string):
    for vr in versions:
        if dump_runs:
            try:
                run = client.get(f"runs/get?run_id={vr['run_id']}")["run"]
                run = dump_run.build_run(run, artifact_max_level, explode_json_string)
                vr["_run"] = run
            except MlflowToolsException:
                print(f"WARNING: Model '{vr.model_name}' version {vr['version']}: run ID {vr['run_id']} does not exist.")
        _format_ts(vr, "creation_timestamp")
        _format_ts(vr, "last_updated_timestamp")


def _adjust_model_timestamps(model):
    tags = model.pop("tags", None)
    latest_versions = model.pop("latest_versions", None)
    _format_ts(model, "creation_timestamp")
    _format_ts(model, "last_updated_timestamp")
    model["tags"] = tags
    model["latest_versions"] = latest_versions


def dump(model_name, 
        format="json", 
        dump_all_versions=False,
        dump_runs=False, 
        explode_json_string = False,
        artifact_max_level = 0,
        output_file=None
    ):

    model = client.get(f"registered-models/get?name={model_name}")
    model = model["registered_model"]
    _adjust_model_timestamps(model)
    if dump_all_versions:
        versions = client.get(f"model-versions/search?name={model_name}")
        versions = versions["model_versions"]
        dump_versions(versions, dump_runs, artifact_max_level, explode_json_string)
        del model["latest_versions"] 
        model["all_versions"] = versions
    else:
        versions =  model.get("latest_versions", None)
        dump_versions(versions, dump_runs, artifact_max_level, explode_json_string)

    dct = { "model": model }
    dump_dct(dct, format)

    if output_file:
        print(f"Writing output to '{output_file}'")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(json.dumps(dct, indent=2)+"\n")


@click.command()
@click.option("--format", 
    help="Output format: json|yaml.",
    type=str,
    default="json"
)
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
@click.option("--explode-json-string",
    help="Explode JSON string.",
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
@click.option("--output-file", 
    help="Output file", 
    type=str,
    required=False,
    show_default=True
)
def main(model, dump_all_versions, dump_runs, format, explode_json_string, artifact_max_level, output_file):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    dump(model, format, dump_all_versions, dump_runs, explode_json_string, artifact_max_level, output_file)


if __name__ == "__main__":
    main()
