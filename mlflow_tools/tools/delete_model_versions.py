"""
Delete a registered model.
"""

import click
import mlflow
from mlflow_tools.common.mlflow_utils import is_unity_catalog_model

client = mlflow.MlflowClient()


def delete_model_versions(model_name, versions):
    """ 
    Delete model versions.
    """
    print(f"Deleting {len(versions)} versions for model '{model_name}'")
    for version in versions:
        try:
            vr = client.get_model_version(model_name, version)
            msg = { "version": vr.version, "stage": vr.current_stage, "status": vr.status, "run_id": vr.run_id }
            print(f"Deleting: {msg}")
            if not is_unity_catalog_model(model_name):
                if vr.current_stage and vr.current_stage != "Archived" and vr.current_stage != "None": # NOTE: for Databricks though OSS works
                    client.transition_model_version_stage (model_name, vr.version, "Archived")
            client.delete_model_version(model_name, vr.version)
        except mlflow.exceptions.RestException as e:
            print(f"ERROR: {e}")


@click.command()
@click.option("--model",
    help="Registered model name", 
    type=str,
    required=True,
)
@click.option("--versions", 
    help="Model versions (comma-delimited)",
    type=str,
    required=True
)
def main(model, versions):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    versions = versions.split(",")
    if len(versions) == 1:
        toks = versions[0].split("-")
        if len(toks) == 2:
            versions = list(range(int(toks[0]), int(toks[1])+1))
    delete_model_versions(model, versions)


if __name__ == "__main__":
    main()
