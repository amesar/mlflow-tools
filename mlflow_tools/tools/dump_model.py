"""
Dump a registered model in JSON or YAML.
"""

import json
import yaml
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

def _dump_dct(dct, format):
    _preprocess(dct)
    if format == "yaml":
        print(yaml.safe_dump(dct))
    else:
        print(json.dumps(dct,indent=2))

def dump(model_name, format, show_runs):
    model = client.get(f"registered-models/get?name={model_name}")
    if show_runs:
        runs = { x['version']:client.get(f"runs/get?run_id={x['run_id']}")['run'] for x in model["registered_model"]["latest_versions"] }
        dct = { "model": model, "version_runs": runs }
        _dump_dct(dct, format)
    else:
        _dump_dct(model, format)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--model", dest="model", help="Registered model name", required=True)
    parser.add_argument("--format", dest="format", help="Format: json|yaml", default="json")
    parser.add_argument("--show_runs", dest="show_runs", help="Show run details", default=False, action='store_true')
    args = parser.parse_args()
    print("Options:")
    for arg in vars(args):
        print("  {}: {}".format(arg,getattr(args, arg)))
    dump(args.model, args.format, args.show_runs)
