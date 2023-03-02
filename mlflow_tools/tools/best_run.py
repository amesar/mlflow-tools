import click
import mlflow
from ..common import mlflow_utils

client = mlflow.client.MlflowClient()

TAG_PARENT_RUN_ID = "mlflow.parentRunId"

def get_best_run(experiment_id_or_name, metric, ascending=False, ignore_nested_runs=False):
    """
    Current search syntax does not allow to check for existence of a tag key so if there are nested runs we have to
    bring all runs back to the client making this costly and unscalable.
    """

    exp = mlflow_utils.get_experiment(client, experiment_id_or_name)
    print("Experiment name:",exp.name)

    order_by = "ASC" if ascending else "DESC"
    column = "metrics.{} {}".format(metric, order_by)
    if ignore_nested_runs:
        runs = client.search_runs(exp.experiment_id, "", order_by=[column])
        runs = [ run for run in runs if TAG_PARENT_RUN_ID not in run.data.tags ]
    else:
        runs = client.search_runs(exp.experiment_id, "", order_by=[column], max_results=1)
    return runs[0].info.run_id,runs[0].data.metrics[metric]

@click.command()
@click.option("--experiment-id-or-name", help="Experiment ID or name.", required=True)
@click.option("--metric", help="Metric.", required=True)
@click.option("--ascending", help="Sort ascending.", type=bool, default=False, show_default=True)
@click.option("--ignore-nested-runs", help="Ignore_nested_runs.", type=bool, default=False, show_default=True)
def main(experiment_id_or_name, metric, ascending, ignore_nested_runs):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    
    best = get_best_run(experiment_id_or_name, metric, ascending, ignore_nested_runs)
    print("Best run:")
    print(f"  run_id: {best[0]}")
    print(f"  {metric}: {best[1]}")

if __name__ == "__main__":
    main()
