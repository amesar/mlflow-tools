"""
List all experiments.
"""

import click
import mlflow
import pandas as pd
from tabulate import tabulate
from mlflow_tools.common.iterators import ListExperimentsIterator
from mlflow_tools.tools.utils import format_time

client = mlflow.client.MlflowClient()
print("MLflow Version:", mlflow.version.VERSION)
print("MLflow Tracking URI:", mlflow.get_tracking_uri())


def to_pandas_dataframe(sort_attribute="name", sort_order="asc", verbose=False):
    exps = [ exp for exp in ListExperimentsIterator(client) ]
    print(f"Found {len(exps)} experiments")
    if sort_attribute == "name":
        exps = sorted(exps, key=lambda x: x.name)
    elif sort_attribute == "experiment_id":
        exps = sorted(exps, key=lambda x: int(x.experiment_id))
    if verbose:
        list = [(exp.experiment_id, exp.name, 
                 format_time(exp.creation_time), format_time(exp.last_update_time), 
                 exp.lifecycle_stage, exp.artifact_location) 
             for exp in exps ]
        columns = ["experiment_id", "name", "creation_time", "last_update_time", "lifecycle_stage", "artifact_location"]
    else:
        list = [(exp.experiment_id, exp.name) for exp in exps ]
        columns = ["experiment_id", "name"]
    df = pd.DataFrame(list, columns=columns)
    if sort_attribute in df.columns:
        df.sort_values(by=[sort_attribute], inplace=True, ascending=sort_order == "asc")
    return df


def list(csv_file, sort_attribute="name", sort_order="asc", verbose=False):
    df = to_pandas_dataframe(sort_attribute, sort_order, verbose)
    with open(csv_file, "w", encoding="utf-8") as f:
        df.to_csv(f, index=False)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


@click.command()
@click.option("--csv-file", help="Output CSV file", default="experiments.csv", show_default=True)
@click.option("--sort-attr", help="Sort by this attibute", default="name", show_default=True)
@click.option("--sort-order", help="Sort order: asc|desc", default="asc", show_default=True)
@click.option("--verbose", help="Verbose", type=bool, default=False, show_default=True)
def main(csv_file, sort_attr, sort_order, verbose):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    list(csv_file, sort_attr, sort_order, verbose)


if __name__ == "__main__":
    main()
