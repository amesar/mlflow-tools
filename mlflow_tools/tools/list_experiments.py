"""
List all experiments.
"""

import click
import mlflow
import pandas as pd
from tabulate import tabulate

client = mlflow.client.MlflowClient()
print("MLflow Version:", mlflow.version.VERSION)
print("MLflow Tracking URI:", mlflow.get_tracking_uri())

max_results = 10000
print("max_results:",max_results)


def fmt(ms):
    import time
    TS_FORMAT = "%Y-%m-%d %H:%M:%S"
    return time.strftime(TS_FORMAT, time.gmtime(round(ms/1000)))


def list(csv_file, sort_attribute="name", sort_order="asc", verbose=False):
    exps = client.search_experiments(max_results=max_results)
    print(f"Found {len(exps)} experiments")

    if sort_attribute == "name":
        exps = sorted(exps, key=lambda x: x.name)
    elif sort_attribute == "experiment_id":
        exps = sorted(exps, key=lambda x: int(x.experiment_id))

    if verbose:
        reverse = sort_order == "desc"
        if sort_attribute == "lifecycle_stage":
            exps = sorted(exps, key=lambda x: x.lifecycle_stage)
        elif sort_attribute == "artifact_location":
            exps = sorted(exps, key=lambda x: x.artifact_location)
        elif sort_attribute == "creation_time":
            exps = sorted(exps, key=lambda x: x.creation_time, reverse=reverse)
        list = [(exp.experiment_id, exp.name, fmt(exp.creation_time), exp.lifecycle_stage, exp.artifact_location) for exp in exps ]
        df = pd.DataFrame(list, columns=["experiment_id","name","creation_time","lifecycle_stage","artifact_location"])
    else:
        list = [(str(exp.experiment_id), exp.name) for exp in exps ]
        df = pd.DataFrame(list,columns=["experiment_id","name"])

    with open(csv_file, "w", encoding="utf-8") as f:
        df.to_csv(f, index=False)

    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    print(f"Found {len(exps)} experiments")


@click.command()
@click.option("--csv-file", help="Output CSV file", default="experiments.csv", show_default=True)
@click.option("--sort-attr", help="Sort by this attibute", default="name", show_default=True)
@click.option("--sort-order", help="Sort by this attibute", default="name", show_default=True)
@click.option("--verbose", help="Verbose", type=bool, default=False, show_default=True)
def main(csv_file, sort_attr, sort_order, verbose):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    list(csv_file, sort_attr, sort_order, verbose)


if __name__ == "__main__":
    main()
