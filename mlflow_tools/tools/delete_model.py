"""
Delete a registered model.
"""

import click
import mlflow
from mlflow_tools.common.iterators import SearchModelVersionsIterator
from mlflow_tools.common.mlflow_utils import is_unity_catalog_model

print("MLflow Tracking URI:", mlflow.get_tracking_uri())
client = mlflow.client.MlflowClient()


def delete_model(model_name, delete_only_versions=False):
    """ 
    Delete a model and all its versions. 
    """
    versions = SearchModelVersionsIterator(client, filter=f"name='{model_name}'")
    versions = list(versions)
    print(f"Deleting {len(versions)} versions for model '{model_name}'")
    for vr in versions:
        msg = { "version": vr.version, "stage": vr.current_stage, "status": vr.status, "run_id": vr.run_id }
        print(f"Deleting: {msg}")
        try:
            if not is_unity_catalog_model(model_name):
                if vr.current_stage and vr.current_stage != "Archived" and vr.current_stage != "None": # NOTE: for Databricks though OSS works
                    client.transition_model_version_stage (model_name, vr.version, "Archived")
            client.delete_model_version(model_name, vr.version)
        except mlflow.MlflowException as e:
            print(f"WARNING: {msg}. Exception: {e}")
    if delete_only_versions:
        print(f"Not deleting model '{model_name}'")
    else:
        print(f"Deleting model '{model_name}'")
        client.delete_registered_model(model_name)


@click.command()
@click.option("--model",
    help="Registered model name", 
    type=str,
    required=True,
)
@click.option("--delete-only-versions", 
    help="Delete only versions and not the registered model",
    type=bool,
    default=False
)
def main(model, delete_only_versions):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    delete_model(model, delete_only_versions)


if __name__ == "__main__":
    main()
