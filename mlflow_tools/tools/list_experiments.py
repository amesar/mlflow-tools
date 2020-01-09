
"""
List all experiments.
"""

import mlflow
import pandas as pd
from tabulate import tabulate

client = mlflow.tracking.MlflowClient()
print("MLflow Version:", mlflow.version.VERSION)
print("MLflow Tracking URI:", mlflow.get_tracking_uri())

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--sort", dest="sort", help="sort", default="name", required=False)
    #parser.add_argument("--sort", dest="sort", help="Sort ", default=False, action='store_true')
    parser.add_argument("--verbose", dest="verbose", help="Show artifacts ", default=False, action='store_true')
    parser.add_argument("--csv_file", dest="csv_file", default="experiments.csv", help="Output CSV file")
    args = parser.parse_args()

    exps = client.list_experiments()
    print("Found {} experiments".format(len(exps)))

    if args.sort == "name":
        exps = sorted(exps, key=lambda x: x.name)
    elif args.sort == "experiment_id":
        exps = sorted(exps, key=lambda x: int(x.experiment_id))

    if args.verbose:
        if args.sort == "lifecycle_stage":
            exps = sorted(exps, key=lambda x: x.lifecycle_stage)
        elif args.sort == "artifact_location":
            exps = sorted(exps, key=lambda x: x.artifact_location)
        list = [(exp.experiment_id, exp.name, exp.lifecycle_stage, exp.artifact_location) for exp in exps ]
        df = pd.DataFrame(list,columns=["experiment_id","name","lifecycle_stage","artifact_location"])
    else:
        list = [(exp.experiment_id, exp.name) for exp in exps ]
        df = pd.DataFrame(list,columns=["experiment_id","name"])

    #print("Output CSV file:",path)
    with open(args.csv_file, 'w') as f:
        df.to_csv(f, index=False)

    print(tabulate(df, headers='keys', tablefmt='psql'))
