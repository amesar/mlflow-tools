"""
List all registered models.
"""

import click
from tabulate import tabulate
from mlflow_tools.api import api_factory
from mlflow_tools.common.click_options import \
    opt_sort_attr, opt_sort_order, opt_output_csv_file

pandas_api = api_factory.get_pandas_api()


def to_pandas_dataframe(sort_attr="name", sort_order="asc"):
    df = pandas_api.search_registered_models(filter=None)
    if sort_attr in df.columns:
        df = df.sort_values(by=[sort_attr], ascending=(sort_order == "asc"))
    return df


def list(csv_file, sort_attr="name", sort_order="asc"):
    df = to_pandas_dataframe(sort_attr, sort_order)
    print(f"Found {df.shape[0]} models")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    if csv_file:
        with open(csv_file, "w", encoding="utf-8") as f:
            df.to_csv(f, index=False)
    print(f"Found {df.shape[0]} models")


@click.command()
@opt_sort_attr
@opt_sort_order
@opt_output_csv_file

def main(sort_attr, sort_order, csv_file):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    list(csv_file, sort_attr, sort_order)


if __name__ == "__main__":
    main()
