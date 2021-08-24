"""
Download the model artifacts associated with a model URI.
"""

import click
from mlflow_tools.common.model_download_utils import download_model

@click.command()
@click.option("--model-uri", help="Model URI", required=True, type=str)
@click.option("--output-dir", help="Output directory for downloaded model", required=True, type=str)
def main(model_uri, output_dir):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")

    if model_uri.startswith("models") or model_uri.startswith("runs"):
        model_path = download_model(model_uri, output_dir)
        print("model_path:",model_path)
    else:
        print(f"ERROR: Unsupported URI: {model_uri}. Must specify a 'models' or 'runs' URI.")

if __name__ == "__main__":
    main()
