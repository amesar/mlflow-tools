"""
List all versions of all registered models with emphasis on if the version's backing run exists.
"""

import click
import pandas as pd
import mlflow
from tabulate import tabulate

client = mlflow.tracking.MlflowClient()


def run(models, get_latest):
    data = []
    for model in models:
        if get_latest:
            versions = client.get_latest_versions(model.name)
        else:
            versions = client.search_model_versions(f"name='{model.name}'")
        vdata = []
        for  vr in versions:
            try:
                run = client.get_run(vr.run_id)
                run_stage = run.info.lifecycle_stage
                run_exists = True
            except mlflow.exceptions.RestException:
                run_exists = False
                run_stage = None
            vdata.append([model.name, vr.version, vr.current_stage, dt(vr.creation_timestamp), vr.run_id, run_stage, run_exists ])
        data = data + vdata
    columns = ["Model","Version","Stage", "Creation", "Run ID", "Run stage", "Run exists"]
    df = pd.DataFrame(data, columns = columns)
    which = "Latest" if get_latest else "All"
    print(f"\n{which} {len(data)} versions")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


def dt(ms):
    from datetime import datetime
    dt = datetime.utcfromtimestamp(ms/1000)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


@click.command()
@click.option("--model", help="Registered model name or 'all' for all models", required=True, type=str)
@click.option("--max-results", help="max_results parameter to MlflowClient.list_registered_models()", default=1000, type=int)
def main(model, max_results):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")

    if model == "all":
        models = client.list_registered_models(max_results=max_results)
    else:
        models = [ client.get_registered_model(model) ]

    run(models, True)
    run(models, False)


if __name__ == "__main__":
    main()
