"""
Count the MLflow objects from MlflowClient search_ methods.
"""

import click
import pandas as pd
from tabulate import tabulate
import mlflow
from  mlflow.exceptions import RestException
from mlflow_tools.api import pandas_api

print("MLflow Tracking URI:", mlflow.get_tracking_uri())


def count(experiments=False, models=False, versions=False, versions_by_models=False, mlflow_api="iterators"):
    mlflow_api = pandas_api.get_api(mlflow_api)
    print("mlflow_api:", mlflow_api)
    data = []
    if experiments:
        data.append([ "experiments", mlflow_api.count_experiments() ])
    if models:
        data.append([ "models", mlflow_api.count_registered_models() ])
    if versions:
        try:
            data.append([ "versions", mlflow_api.count_model_versions() ])
        except RestException as e:
            #print("ERROR: versions count:",e)
            data.append([ "versions", str(e)])
    if versions_by_models:
        data.append([ "versions by models", mlflow_api.count_model_versions_by_models() ])
    df = pd.DataFrame(data, columns = ["Object","Count"])
    print("\nMLflow object counts")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


@click.command()
@click.option("--experiments", help="Experiments count", type=bool, is_flag=True)
@click.option("--models", help="Registered models count", type=bool, is_flag=True)
@click.option("--versions", help="Model versions count", type=bool, is_flag=True)
@click.option("--versions-by-models", help="Model versions by models count", type=bool, is_flag=True)
@click.option("--mlflow-api", help="MLflowApi implementation: iterator|list", default="iterator", show_default=True)
def main(experiments, models, versions, versions_by_models, mlflow_api):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    count(experiments, models, versions, versions_by_models, mlflow_api)


if __name__ == "__main__":
    main()
