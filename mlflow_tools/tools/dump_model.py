"""
Dump a registered model in JSON or YAML.
"""

import click
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.common.http_client import MlflowHttpClient
from mlflow_tools.tools.utils import format_time
from . import dump_dct, dump_run

client = MlflowHttpClient()


def _format_dt(dct, key):
    v = dct.get(key,None)
    if v: 
        dct[f"_{key}"] = format_time(int(v))


def _preprocess(dct):
    dct =  dct["registered_model"]
    _format_dt(dct, "creation_timestamp")
    _format_dt(dct, "last_updated_timestamp")
    latest_versions = dct.get("latest_versions",None)
    if latest_versions:
        for v in latest_versions:
            _format_dt(v, "creation_timestamp")
            _format_dt(v, "last_updated_timestamp")


def dump(model_name, format="json", show_runs=False, format_datetime=False, explode_json_string=False, artifact_max_level=0):
    model = client.get(f"registered-models/get?name={model_name}")
    if format_datetime:
        _preprocess(model)
    if show_runs:
        latest_versions =  model["registered_model"].get("latest_versions",None)
        if latest_versions:
            #vruns = { vr['version']:client.get(f"runs/get?run_id={vr['run_id']}")['run'] for vr in latest_versions }
            vruns = {}
            for vr in latest_versions:
                try:
                    run = client.get(f"runs/get?run_id={vr['run_id']}")
                    vruns[vr['version']] = run['run']
                except MlflowToolsException:
                    print(f"WARNING: Model '{model_name}' version {vr['version']}: run ID {vr['run_id']} does not exist.")
                    #print(e)
                    # HTTP status code: 404
            if format_datetime or explode_json_string or artifact_max_level > 0:
                for k,run in vruns.items():
                    vruns[k] = dump_run.build_run(run, artifact_max_level, explode_json_string)
            dct = { "model": model, "version_runs": vruns }
        else:
            dct = { "model": model }
        dump_dct(dct,format)
    else:
        dct = model
        dump_dct(dct, format)
    return dct


@click.command()
@click.option("--format", 
    help="Output format: json|yaml.",
    type=str,
    default="json"
)
@click.option("--model",
     help="Registered model name.",
     required=True, type=str
)
@click.option("--show-runs",
    help="Show run details.",
    type=bool,
    default=False, 
    show_default=True
)
@click.option("--format-datetime",
    help="Show human-readable datetime formats.",
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
def main(model, show_runs, format, format_datetime, explode_json_string, artifact_max_level
):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    dump(model, format, show_runs, format_datetime, explode_json_string, artifact_max_level)


if __name__ == "__main__":
    main()
