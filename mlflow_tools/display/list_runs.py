"""
List runs.
"""

import click
from tabulate import tabulate
import mlflow
from mlflow.entities import ViewType
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.common import mlflow_utils
from mlflow_tools.common.click_options import \
    opt_experiment_id_or_name, \
    opt_sort_attr, opt_sort_order, opt_view_type, \
    opt_columns, opt_output_csv_file
from mlflow_tools.api import api_factory
from mlflow_tools.display.display_utils import process_df

pandas_api = api_factory.get_pandas_api()
mlflow_client = mlflow.client.MlflowClient()


def to_pandas_dataframe(
        experiment_id_or_name, 
        view_type=None, 
        filter=None
    ):
    return pandas_api.search_runs(experiment_id_or_name, view_type=view_type, filter=filter)


def list(experiment_id_or_name, sort_attr="name", sort_order="asc", view_type=None, filter=None, columns=None, csv_file=None):
    exp = mlflow_utils.get_experiment(mlflow_client, experiment_id_or_name)
    if exp is None:
        raise MlflowToolsException(f"Cannot find experiment '{experiment_id_or_name}'")
    df = to_pandas_dataframe(exp.experiment_id, view_type, filter)
    df = process_df(df, columns, sort_attr, sort_order, csv_file)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    print(f"Runs: {df.shape[0]}")


@click.command()
@opt_experiment_id_or_name
@opt_sort_attr
@opt_sort_order
@opt_view_type
@opt_columns
@opt_output_csv_file

def main(experiment_id_or_name, sort_attr, sort_order, view_type, columns, csv_file):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    if view_type:
        view_type = ViewType.from_string(view_type)
    if columns:
        columns = columns.split(",")
    list(experiment_id_or_name, sort_attr, sort_order, view_type=view_type, 
        columns=columns, csv_file=csv_file
    )


if __name__ == "__main__":
    main()
