"""
Delete a registered model.
"""

import click
import mlflow
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.common.click_options import opt_experiment_id_or_name
from mlflow_tools.common import mlflow_utils
from mlflow_tools.common.iterators import SearchRunsIterator

print("MLflow Tracking URI:", mlflow.get_tracking_uri())
client = mlflow.MlflowClient()


def delete_experiment(experiment_id_or_name, delete_only_runs):
    exp = mlflow_utils.get_experiment(client, experiment_id_or_name)
    if exp is None:
        raise MlflowToolsException(f"Cannot find experiment '{experiment_id_or_name}'")
    if delete_only_runs:
        runs = SearchRunsIterator(client, [exp.experiment_id])
        runs = list(runs)
        print(f"Deleting {len(runs)} runs")
        for run in runs:
            client.delete_run(run.info.run_id)
    else:
        client.delete_experiment(exp.experiment_id)


@click.command()
@opt_experiment_id_or_name
@click.option("--delete-only-runs", 
    help="Delete only runs and not the experiment",
    type=bool,
    default=False,
    show_default=True
)
def main(experiment_id_or_name, delete_only_runs):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    delete_experiment(experiment_id_or_name, delete_only_runs)


if __name__ == "__main__":
    main()
