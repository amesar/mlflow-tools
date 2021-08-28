"""
Dump a registered model in JSON or YAML.
"""

import json
import yaml
import click
from mlflow_tools.common.http_client import MlflowHttpClient
from . import format_dt, dump_dct
from . import dump_run

client = MlflowHttpClient()

def _format_dt(dct, key):
    v = dct.get(key,None)
    if v: 
        dct[f"_{key}"] = format_dt(int(v))

def _preprocess(dct):
    dct =  dct["registered_model"]
    _format_dt(dct, "creation_timestamp")
    _format_dt(dct, "last_updated_timestamp")
    for v in dct["latest_versions"]:
        _format_dt(v, "creation_timestamp")
        _format_dt(v, "last_updated_timestamp")

def dump(model_name, format, show_runs, format_datetime, explode_json_string, artifact_max_level):
    model = client.get(f"registered-models/get?name={model_name}")
    if format_datetime:
        _preprocess(model)
    if show_runs:
        vruns = { x['version']:client.get(f"runs/get?run_id={x['run_id']}")['run'] for x in model["registered_model"]["latest_versions"] }
        if format_datetime or explode_json_string or artifact_max_level > 0:
            for k,run in vruns.items():
                vruns[k] = dump_run.build_run(run, artifact_max_level, explode_json_string)
        dct = { "model": model, "version_runs": vruns }
        dump_dct(dct,format)
    else:
        dump_dct(model, format)

@click.command()
@click.option("--format", help="Output format: json|yaml.", default="name")
@click.option("--model", help="Registered model name.", required=True, type=str)
@click.option("--show-runs", help="Show run details.", type=bool, default=False, show_default=False)
@click.option("--format-datetime", help="Show human-readable datetime formats.", type=bool, default=False, show_default=False)
@click.option("--explode-json-string", help="Explode JSON string.", type=bool, default=False, show_default=True)
@click.option("--artifact-max-level", help="Number of artifact levels to recurse.", default=0, type=int)

def main(model, show_runs, format, format_datetime, explode_json_string, artifact_max_level):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    dump(model, format, show_runs, format_datetime, explode_json_string, artifact_max_level)

if __name__ == "__main__":
    main()
