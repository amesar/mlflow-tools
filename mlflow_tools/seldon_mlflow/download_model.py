"""
Replace a non-file MLflow URI (models: or runs: scheme) with the downloaded file path since Seldon MLServer only accepts file paths.
"""

import os
import shutil
import json
import click
from mlflow_tools.common.model_download_utils import download_model

@click.command()
@click.option("--model-settings-path", help="Path to source model-settings file", required=True, type=str)
@click.option("--output-dir", help="Output directory for downloaded model", required=True, type=str)
def main(model_settings_path, output_dir):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")

    os.makedirs(output_dir, exist_ok=True)
    with open(model_settings_path, "r") as f:
        dct = json.loads(f.read())
    model_uri = dct["parameters"]["uri"]
    print("model_uri:",model_uri)

    if model_uri.startswith("runs") or model_uri.startswith("models"):
        model_path = download_model(model_uri, output_dir)
        print("model_path:",model_path)
        dct["parameters"]["uri"] = model_path
        with open("model-settings.json", "w") as f:
            f.write(json.dumps(dct,indent=4)+"\n")
    else:
        model_path = model_uri
        shutil.copyfile(model_settings_path, "model-settings.json")

if __name__ == "__main__":
    main()
