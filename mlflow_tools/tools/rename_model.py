"""
Rename a registered model.
"""

import click
import mlflow
from mlflow_tools.common.mlflow_utils import is_unity_catalog_model

print("MLflow Tracking URI:", mlflow.get_tracking_uri())
client = mlflow.client.MlflowClient()


def rename_model(model_name, new_model_name, fudge_version_stage=True):
    print(f"Renaming model '{model_name}' to '{new_model_name}'")
    if not fudge_version_stage:
        client.rename_registered_model(model_name, new_model_name)
        return 

    model = client.get_registered_model(model_name)

    if model.latest_versions: # if non-UC
        print(f"Transitioning versions temporarily for model '{model_name}' to 'Archived' stage in order to rename model")
        for vr in model.latest_versions:
            print(f'  {{"version": {vr.version}, "stage": {vr.current_stage}}}')
            if not is_unity_catalog_model(model_name):
                if vr.current_stage != "Archived":
                    client.transition_model_version_stage(model_name, vr.version, "Archived")

    client.rename_registered_model(model_name, new_model_name)

    if not is_unity_catalog_model(model_name):
        if model.latest_versions: # if non-UC
            print(f"Transitioning versions for model '{new_model_name}' back to original stage")
            for vr in model.latest_versions:
                print(f'  {{"version": {vr.version}, "stage": {vr.current_stage}}}')
                if vr.current_stage != "Archived":
                    client.transition_model_version_stage(new_model_name, vr.version, vr.current_stage)


@click.command()
@click.option("--model", 
    help="Model name to rename", 
    type=str,
    required=True,
)
@click.option("--new-model", 
    help="New model name", 
    type=str,
    required=True,
)
@click.option("--fudge-version-stage", 
    help="Fudge version stage: Transition stage to 'Archived' before delete, and then restore original version stage for new model.", 
    type=bool, 
    default=True, 
    show_default=True
)

def main(model, new_model, fudge_version_stage):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    rename_model(model, new_model, fudge_version_stage)


if __name__ == "__main__":
    main()
