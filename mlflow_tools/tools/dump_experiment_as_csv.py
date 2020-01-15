
import mlflow
from tabulate import tabulate
from ..common import mlflow_utils

client = mlflow.tracking.MlflowClient()
print("MLflow Version:", mlflow.version.VERSION)
print("MLflow Tracking URI:", mlflow.get_tracking_uri())

def dump_experiment(experiment_id_or_name, csv_file):
    exp = mlflow_utils.get_experiment(client, experiment_id_or_name)
    pdf = mlflow.search_runs([exp.experiment_id], "")
    print(tabulate(pdf, headers='keys', tablefmt='psql'))
    if csv_file is None: 
        csv_file = f"experimenty_{exp.experiment_id}.csv"
    with open(csv_file, "w") as f:
        pdf.to_csv(f, index=False)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--experiment_id_or_name", dest="experiment_id_or_name", help="Experiment ID or name", required=True)
    parser.add_argument("--csv_file", dest="csv_file", help="csv_file", default=None, required=False)
    args = parser.parse_args()
    print("Arguments:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")
    dump_experiment(args.experiment_id_or_name, args.csv_file)
