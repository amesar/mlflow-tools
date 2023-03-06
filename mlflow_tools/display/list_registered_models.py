"""
List all registered models.
"""

import click
from tabulate import tabulate
from mlflow_tools.api import api_factory

pandas_api = api_factory.get_pandas_api()

def to_pandas_dataframe(sort_attribute="name", sort_order="asc"):
    df = pandas_api.search_registered_models(filter=None)
    if sort_attribute in df.columns:
        df = df.sort_values(by=[sort_attribute], ascending=(sort_order == "asc"))
    return df


def list(csv_file, sort_attribute="name", sort_order="asc"):
    df = to_pandas_dataframe(sort_attribute, sort_order)
    print(f"Found {df.shape[0]} models")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    with open(csv_file, "w", encoding="utf-8") as f:
        df.to_csv(f, index=False)
    print(f"Found {df.shape[0]} models")


@click.command()
@click.option("--csv-file", help="Output CSV file", default="models.csv", show_default=True)
@click.option("--sort-attr", help="Sort by this attibute", default="name", show_default=True)
@click.option("--sort-order", help="Sort order: asc|desc", default="asc", show_default=True)
def main(csv_file, sort_attr, sort_order):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    list(csv_file, sort_attr, sort_order)


if __name__ == "__main__":
    main()
