"""
Delete a registered model.
"""

import click
import mlflow

print("MLflow Tracking URI:", mlflow.get_tracking_uri())


def delete_model(model_name, delete_only_versions=False, client=None):
    """ Delete a model and all its versions. """
    if not client:
        client = mlflow.client.MlflowClient()
    versions = client.search_model_versions(f"name='{model_name}'") # TODO: handle page token
    print(f"Deleting {len(versions)} versions for model '{model_name}'")
    for vr in versions:
        print(f"Deleting version={vr.version} stage={vr.current_stage} status={vr.status} run_id={vr.run_id}")
        if vr.current_stage != "Archived": # NOTE: for Databricks though OSS works
            client.transition_model_version_stage (model_name, vr.version, "Archived")
        client.delete_model_version(model_name, vr.version)
    if not delete_only_versions:
        client.delete_registered_model(model_name)


@click.command()
@click.option("--model", help="Registered model name", required=True, type=str)
@click.option("--delete-only-versions", help="Delete only versions and not the registered model", default=False, type=bool)
def main(model, delete_only_versions):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    delete_model(model, delete_only_versions)


if __name__ == "__main__":
    main()
