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

@click.command()
@click.option("--csv-file", help="Output CSV file", default="experiments.csv")
@click.option("--sort", help="Sort by this attibute", default="name")
@click.option("--verbose", help="Show artifacts", type=bool, default=False, show_default=False)
def main(csv_file, sort, verbose):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")

    exps = client.list_experiments()
    print("Found {} experiments".format(len(exps)))

    if sort == "name":
        exps = sorted(exps, key=lambda x: x.name)
    elif sort == "experiment_id":
        exps = sorted(exps, key=lambda x: int(x.experiment_id))

    if verbose:
        if sort == "lifecycle_stage":
            exps = sorted(exps, key=lambda x: x.lifecycle_stage)
        elif sort == "artifact_location":
            exps = sorted(exps, key=lambda x: x.artifact_location)
        list = [(exp.experiment_id, exp.name, exp.lifecycle_stage, exp.artifact_location) for exp in exps ]
        df = pd.DataFrame(list,columns=["experiment_id","name","lifecycle_stage","artifact_location"])
    else:
        list = [(exp.experiment_id, exp.name) for exp in exps ]
        df = pd.DataFrame(list,columns=["experiment_id","name"])

    with open(csv_file, 'w') as f:
        df.to_csv(f, index=False)

    print(tabulate(df, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    main()
