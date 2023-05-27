""" Dump experiment runs as CSV """

import click
import mlflow
from tabulate import tabulate
from mlflow_tools.common.click_options import (
    opt_experiment_id_or_name,
    opt_output_csv_file
)
from ..common import mlflow_utils

client = mlflow.MlflowClient()

def dump_experiment(experiment_id_or_name, csv_file):
    exp = mlflow_utils.get_experiment(client, experiment_id_or_name)
    pdf = mlflow.search_runs([exp.experiment_id], "")
    print(tabulate(pdf, headers='keys', tablefmt='psql'))
    if csv_file is None: 
        csv_file = f"experimenty_{exp.experiment_id}.csv"
    with open(csv_file, "w", encoding="utf-8") as f:
        pdf.to_csv(f, index=False)


@click.command()
@opt_experiment_id_or_name
@opt_output_csv_file

def main(experiment_id_or_name, csv_file):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    dump_experiment(experiment_id_or_name, csv_file)


if __name__ == "__main__":
    main()
