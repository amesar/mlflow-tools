"""
Delete a registered model.
"""

import mlflow
from mlflow_tools.common import model_utils

client = mlflow.tracking.MlflowClient()
print("MLflow Tracking URI:", mlflow.get_tracking_uri())

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--model", dest="model", help="Registered model name", required=True)
    args = parser.parse_args()
    print("Options:")
    for arg in vars(args):
        print("  {}: {}".format(arg,getattr(args, arg)))
    model_utils.delete_model(client, args.model)
