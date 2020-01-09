
import mlflow
from tabulate import tabulate

client = mlflow.tracking.MlflowClient()
print("MLflow Version:", mlflow.version.VERSION)
print("MLflow Tracking URI:", mlflow.get_tracking_uri())

def dump_experiment(exp_id, csv_file):
    pdf = mlflow.search_runs([exp_id], "")
    print(tabulate(pdf, headers='keys', tablefmt='psql'))
    with open(csv_file, "w") as f:
        pdf.to_csv(f, index=False)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    #parser.add_argument("--experiment_id_or_name", dest="experiment_id", help="Experiment ID", required=True)
    parser.add_argument("--experiment_id", dest="experiment_id", help="Experiment ID", required=True)
    parser.add_argument("--csv_file", dest="csv_file", help="csv_file", default="out.csv", required=False)
    args = parser.parse_args()
    print("args:",args)
    dump_experiment(args.experiment_id, args.csv_file)
