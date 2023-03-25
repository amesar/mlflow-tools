"""
List all registered models.
"""

import click
from tabulate import tabulate
from mlflow_tools.api import api_factory
from mlflow_tools.common.click_options import \
    opt_sort_attr, opt_sort_order, opt_columns, opt_output_csv_file
from mlflow_tools.display.display_utils import process_df

pandas_api = api_factory.get_pandas_api()


def to_pandas_dataframe(filter=None):
    return pandas_api.search_registered_models(filter=filter)


def list(sort_attr="name", sort_order="asc", columns=None, csv_file=None):
    df = to_pandas_dataframe(filter=None)
    print(f"Found {df.shape[0]} models")
    df = process_df(df, columns, sort_attr, sort_order, csv_file)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    print(f"Found {df.shape[0]} models")


@click.command()
@opt_sort_attr
@opt_sort_order
@opt_columns
@opt_output_csv_file

def main(sort_attr, sort_order, columns, csv_file):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    if columns:
        columns = columns.split(",")
    list(sort_attr, sort_order, columns, csv_file)


if __name__ == "__main__":
    main()
