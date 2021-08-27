"""
Delete a registered model.
"""

import click
import mlflow
from mlflow_tools.common import model_utils

client = mlflow.tracking.MlflowClient()
print("MLflow Tracking URI:", mlflow.get_tracking_uri())

@click.command()
@click.option("--model", help="Registered model name", required=True, type=str)
def main(model):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    model_utils.delete_model(client, model)

if __name__ == "__main__":
    main()
