"""
List all versions of all registered models with info if the version's backing run exists.
"""

import click
import pandas as pd
import mlflow
from tabulate import tabulate
from mlflow_tools.common.mlflow_utils import get_model_versions
from mlflow_tools.tools.utils import format_time

client = mlflow.tracking.MlflowClient()


def mk_versions_pandas_df(models, get_latest_versions):
    data = []
    model_names = [ m.name for m in models ]
    for model_name in model_names:
        versions = get_model_versions(client, model_name, get_latest_versions)
        vdata = []
        for  vr in versions:
            try:
                run = client.get_run(vr.run_id)
                run_stage = run.info.lifecycle_stage
                run_exists = True
            except mlflow.exceptions.RestException:
                run_exists = False
                run_stage = None
            vdata.append([
                model_name,
                vr.version,
                vr.current_stage,
                format_time(vr.creation_timestamp),
                format_time(vr.last_updated_timestamp),
                vr.run_id,
                run_stage,
                run_exists 
            ])
        data = data + vdata
    columns = ["Model", "Version", "Stage", "Creation", "Last Updated", "Run ID", "Run stage", "Run exists"]
    df = pd.DataFrame(data, columns = columns)
    return df


def show_versions(models, get_latest_versions):
    df = mk_versions_pandas_df(models, get_latest_versions)
    which = "Latest" if get_latest_versions else "All"
    print(f"\n{which} {df.shape[0]} versions")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


def run(model, view, max_results):
    models1 = client.search_registered_models(max_results=max_results)
    models2 = [ client.get_registered_model(model) ]
    if model == "all":
        models = client.search_registered_models(max_results=max_results)
    else:
        models = [ client.get_registered_model(model) ]
    if view in ["latest","both"]:
        show_versions(models, True)
    if view in ["all","both"]:
        show_versions(models, False)
    if view not in ["latest", "all","both"]:
        print(f"ERROR: Bad 'view' value '{view}'")


@click.command()
@click.option("--model", 
  help="Registered model name or 'all' for all models.", 
  type=str,
  required=True
)
@click.option("--view", 
  help="Display latest, all or both views of versions. Values are: 'latest|all|both'.", 
  type=str,
  default="latest", 
  show_default=True
)
@click.option("--max-results", 
  help="max_results parameter to MlflowClient.search_registered_models().", 
  type=int,
  default=1000,
  show_default=True
)
def main(model, view, max_results):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    run(model, view, max_results
)
if __name__ == "__main__":
    main()
