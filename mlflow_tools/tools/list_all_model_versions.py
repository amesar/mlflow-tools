"""
List all versions of all registered models with emphasis on if the version's backing run exists.
"""

import sys
import click
import pandas as pd
import mlflow
from tabulate import tabulate

client = mlflow.tracking.MlflowClient()

@click.command()
@click.option("--format", help="text|csv", default="text", type=str)
@click.option("--max-results", help="max_results parameter to MlflowClient.list_registered_models()", default=1000, type=int)

def main(format, max_results):
    models = client.list_registered_models(max_results=max_results)
    data = []
    for model in models:
        versions = client.search_model_versions(f"name='{model.name}'")
        vdata = []
        for  vr in versions:
            try:
                client.get_run(vr.run_id)
                run_exists = True
            #except mlflow.exceptions.RestException:
            except Exception:
                run_exists = False
            vdata.append([model.name, vr.version, vr.current_stage, vr.run_id, run_exists ])
        data = data + vdata
    columns = ["Model","Version","Stage", "Run ID", "Run exists"]
    df = pd.DataFrame(data, columns = columns)
    if format.lower() == "csv":
        print(df.to_csv(sys.stdout, index=False))
    else:
        print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))

if __name__ == "__main__":
    main()
