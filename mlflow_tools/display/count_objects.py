"""
Count the MLflow objects from MlflowClient search_ methods.
"""

import click
import pandas as pd
from tabulate import tabulate
import mlflow
from  mlflow.exceptions import RestException
from mlflow_tools.api.api_factory import MLFLOW_API_ITERATOR, MLFLOW_API_SEARCH, DEFAULT_MLFLOW_API
from mlflow_tools.api import api_factory

print("MLflow Tracking URI:", mlflow.get_tracking_uri())


def _build_count(mlflow_api=DEFAULT_MLFLOW_API, experiments=False, models=False, versions=False, versions_by_models=False):
    mlflow_api = api_factory.get_mlflow_api(mlflow_api)
    print("mlflow_api:", type(mlflow_api))
    data = []
    if experiments:
        data.append([ "experiments", mlflow_api.count_experiments() ])
    if models:
        data.append([ "models", mlflow_api.count_registered_models() ])
    if versions:
        try:
            data.append([ "versions", mlflow_api.count_model_versions() ])
        except RestException as e:
            data.append([ "versions", str(e)])
    if versions_by_models:
        data.append([ "versions (by models)", mlflow_api.count_model_versions_by_models() ])
    return data


def count_impl(mlflow_api=DEFAULT_MLFLOW_API, experiments=False, models=False, versions=False, versions_by_models=False):
    data = _build_count(mlflow_api, experiments, models, versions, versions_by_models)
    df = pd.DataFrame(data, columns = ["Object","Count"])
    print(f"\nObject counts for '{mlflow_api}' implementation")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))

def count_comparison(experiments=False, models=False, versions=False, versions_by_models=False):
    data1 = _build_count(MLFLOW_API_ITERATOR, experiments, models, versions, versions_by_models)
    data2 = _build_count(MLFLOW_API_SEARCH,   experiments, models, versions, versions_by_models)
    data = [ [ d1[0], d1[1], d2[1] ] for d1, d2 in zip(data1,data2) ]
    df = pd.DataFrame(data, columns = ["Mlflow object", "Iterator", "List"])
    print("\nMLflow object count comparison")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


def count(mlflow_api=DEFAULT_MLFLOW_API, experiments=False, models=False, versions=False, versions_by_models=False):
    if mlflow_api == "both":
        count_comparison(experiments, models, versions, versions_by_models)
    else:
        count_impl(mlflow_api, experiments, models, versions, versions_by_models)


@click.command()
@click.option("--experiments", help="Experiments count", type=bool, is_flag=True)
@click.option("--models", help="Registered models count", type=bool, is_flag=True)
@click.option("--versions", help="Model versions count", type=bool, is_flag=True)
@click.option("--versions-by-models", help="Model versions (by models count)", type=bool, is_flag=True)
@click.option("--mlflow-api", 
    help=f"MLflowApi implementation: {MLFLOW_API_ITERATOR}|{MLFLOW_API_SEARCH}|both.\
        '{MLFLOW_API_SEARCH}' directly calls MlflowClient.search methods.\
        '{MLFLOW_API_ITERATOR}' calls wrapper with page token. 'both' compares the two.", 
    default=DEFAULT_MLFLOW_API,
    show_default=True
)
def main(experiments, models, versions, versions_by_models, mlflow_api):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    count(mlflow_api, experiments, models, versions, versions_by_models)


if __name__ == "__main__":
    main()
