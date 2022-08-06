"""
List the versions of a registered model.
"""

import click
import pandas as pd
import mlflow
from tabulate import tabulate

client = mlflow.tracking.MlflowClient()
print("MLflow Tracking URI:", mlflow.get_tracking_uri())

@click.command()
@click.option("--model", help="Registered model name", required=True, type=str)

def main(model):
    print("\nModel:",model)

    versions = client.get_latest_versions(model)
    versions = sorted(versions, key=lambda x: x.current_stage, reverse=True)
    show_versions(versions, f"\nLatest {len(versions)} versions")

    versions = client.search_model_versions(f"name='{model}'")
    versions = sorted(versions, key=lambda x: x.current_stage, reverse=True)
    show_versions(versions, f"\nAll {len(versions)} versions")

def show_versions(versions, msg):
    versions = [ [vr.version, vr.current_stage, vr.status, dt(vr.creation_timestamp) ] for vr in versions ]
    columns = ["Version","Stage", "Status", "Creation"]
    df = pd.DataFrame(versions, columns = columns)
    print(msg)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))

def dt(ms):
    from datetime import datetime
    dt = datetime.utcfromtimestamp(ms/1000)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    main()
