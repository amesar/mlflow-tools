"""
Delete versions of the specified stage of registered model.
"""

import click
import mlflow
from mlflow_tools.tools import utils 

client = mlflow.tracking.MlflowClient()
print("MLflow Tracking URI:", mlflow.get_tracking_uri())


@click.command()
@click.option("--model", help="Registered model name", required=True, type=str)
@click.option("--stages", help="Stages to export (comma seperated). Default is all stages.", default="", required=False, type=str)
def main(model, stages):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    stages = utils.normalize_stages(stages)
    versions = client.search_model_versions(f"name='{model}'")
    print(f"Found {len(versions)} versions for model {model}")
    for vr in versions:
        if len(stages) == 0 or vr.current_stage.lower() in stages:
            dct = { "version": vr.version, "stage": vr.current_stage, "run_id": vr.run_id }
            print(f"Deleting {dct}")
            client.delete_model_version(model, vr.version)


if __name__ == "__main__":
    main()
