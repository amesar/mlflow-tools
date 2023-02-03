"""
List all registered models.
"""

import click
import pandas as pd
import mlflow
from tabulate import tabulate
from mlflow_tools.tools.utils import format_time
from mlflow_tools.common.iterators import SearchRegisteredModelsIterator

client = mlflow.tracking.MlflowClient()


def to_pandas_dataframe(sort_attribute="name", sort_order="asc"):
    models = [ m for m in SearchRegisteredModelsIterator(client) ]
    list = [ [ m.name, len(m.latest_versions), 
               format_time(m.creation_timestamp), format_time(m.last_updated_timestamp), 
               m.description ] 
        for m in models ]
    columns = ["name", "versions", "creation_timestamp", "last_updated_timestamp", "description" ]
    df = pd.DataFrame(list, columns=columns)
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
