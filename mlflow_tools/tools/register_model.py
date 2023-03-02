
"""
Register a run's model as a registered model version and optional stage.
"""

import click
import mlflow
from mlflow.exceptions import RestException

@click.command()
@click.option("--registered-model", help="New registered model name.", required=True, type=str)
@click.option("--run-id", help="Run ID", required=True, type=str)
@click.option("--model-artifact", help="Source relative model artifact path.", required=True, type=str)
@click.option("--stage", help="Stage", default=None, type=str)

def main(registered_model, run_id, model_artifact, stage):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    client = mlflow.client.MlflowClient()
    try:
        client.create_registered_model(registered_model)
        print(f"Created new model '{registered_model}'")
    except RestException as e:
        if not "RESOURCE_ALREADY_EXISTS: Registered Model" in str(e):
            raise e
        print(f"Model '{registered_model}' already exists")

    run = client.get_run(run_id)
    source = f"{run.info.artifact_uri}/{model_artifact}"
    print("Source:",source)

    version = client.create_model_version(registered_model, source, run_id)
    print("Version:",version)

    if stage:
        client.transition_model_version_stage(registered_model, version.version, stage)

if __name__ == "__main__":
    main()
