"""
List all experiments.
"""

import click
import mlflow
import pandas as pd
from tabulate import tabulate

client = mlflow.tracking.MlflowClient()
print("MLflow Version:", mlflow.version.VERSION)
print("MLflow Tracking URI:", mlflow.get_tracking_uri())

def list(csv_file, sort_attribute="name", verbose=False):
    exps = client.search_experiments()
    print("Found {} experiments".format(len(exps)))

    if sort_attribute == "name":
        exps = sorted(exps, key=lambda x: x.name)
    elif sort_attribute == "experiment_id":
        exps = sorted(exps, key=lambda x: int(x.experiment_id))

    if verbose:
        if sort_attribute == "lifecycle_stage":
            exps = sorted(exps, key=lambda x: x.lifecycle_stage)
        elif sort_attribute == "artifact_location":
            exps = sorted(exps, key=lambda x: x.artifact_location)
        list = [(exp.experiment_id, exp.name, exp.lifecycle_stage, exp.artifact_location) for exp in exps ]
        df = pd.DataFrame(list,columns=["experiment_id","name","lifecycle_stage","artifact_location"])
    else:
        list = [(exp.experiment_id, exp.name) for exp in exps ]
        df = pd.DataFrame(list,columns=["experiment_id","name"])

    with open(csv_file, "w", encoding="utf-8") as f:
        df.to_csv(f, index=False)

    print(tabulate(df, headers='keys', tablefmt='psql'))

@click.command()
@click.option("--csv-file", help="Output CSV file", default="experiments.csv", show_default=True)
@click.option("--sort", help="Sort by this attibute", default="name", show_default=True)
@click.option("--verbose", help="Verbose", type=bool, default=False, show_default=True)

def main(csv_file, sort, verbose):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    list(csv_file, sort, verbose)

if __name__ == "__main__":
    main()
