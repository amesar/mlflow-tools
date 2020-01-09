import mlflow
from ..common import mlflow_utils

client = mlflow.tracking.MlflowClient()

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

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    #parser.add_argument("--experiment_id", dest="experiment_id", help="Experiment ID", type=str, required=True)
    parser.add_argument("--experiment_id_or_name", dest="experiment_id_or_name", help="Experiment ID", required=True)
    parser.add_argument("--metric", dest="metric", help="Metric", type=str, required=True)
    parser.add_argument("--ascending", dest="ascending", help="ascending", required=False, default=False, action="store_true")
    parser.add_argument("--ignore_nested_runs", dest="ignore_nested_runs", help="Ignore nested runs", required=False, default=False, action="store_true")
    args = parser.parse_args()
    print("Arguments:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")
    best = get_best_run(args.experiment_id_or_name, args.metric, args.ascending, args.ignore_nested_runs)
    print("Best:",best)
