"""
Dump a registered model in JSON or YAML.
"""

import json
import yaml
import click
from mlflow_tools.common.http_client import MlflowHttpClient
from . import format_dt

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

def _dump_dct(dct, format, format_datetime):
    if format_datetime:
        _preprocess(dct)
    if format == "yaml":
        print(yaml.safe_dump(dct))
    else:
        print(json.dumps(dct,indent=2))

def dump(model_name, format, show_runs, format_datetime):
    model = client.get(f"registered-models/get?name={model_name}")
    if show_runs:
        runs = { x['version']:client.get(f"runs/get?run_id={x['run_id']}")['run'] for x in model["registered_model"]["latest_versions"] }
        dct = { "model": model, "version_runs": runs }
        _dump_dct(dct, format, format_datetime)
    else:
        _dump_dct(model, format, format_datetime)

@click.command()
@click.option("--format", help="Output format: json|yaml", default="name")
@click.option("--model", help="Registered model name", required=True, type=str)
@click.option("--show-runs", help="Show run details", type=bool, default=False, show_default=False)
@click.option("--format-datetime", help="Show human-readable datetime formats", type=bool, default=False, show_default=False)
def main(model, show_runs, format, format_datetime):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    dump(model, format, show_runs, format_datetime)

if __name__ == "__main__":
    main()
