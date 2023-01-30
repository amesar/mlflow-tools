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


def mk_versions_pandas_df(models, get_latest_versions=False):
    table = []
    if isinstance(models,str):
        model_names = [ models ]
    else:
        if len(models) == 0:
            model_names = []
        elif not isinstance(models[0], str):
            model_names = [ m.name for m in models ]
        else:
            model_names = models
    for model_name in model_names:
        versions = get_model_versions(client, model_name, get_latest_versions)
        vtable = []
        for  vr in versions:
            try:
                run = client.get_run(vr.run_id)
                run_stage = run.info.lifecycle_stage
                run_exists = True
            except mlflow.exceptions.RestException:
                run_exists = False
                run_stage = None
            row = [
                vr.version,
                vr.current_stage,
                format_time(vr.creation_timestamp),
                format_time(vr.last_updated_timestamp),
                vr.run_id,
                run_stage,
                run_exists 
            ]
            if len(models) > 1:
                row = [ vr.name ] + row
            vtable.append(row)
        table = table + vtable
    columns = ["Version", "Stage", "Creation", "Last Updated", "Run ID", "Run stage", "Run exists"]
    if len(models) > 1:
        columns = ["Model" ] + columns
        df = pd.DataFrame(table, columns = columns)
        df = df.sort_values(by=["Model", "Version"], ascending=False)
    else:
        columns = ["Model" ] + columns
        df = pd.DataFrame(table, columns = columns)
        df = df.sort_values(by=["Version"], ascending=False)
    return df


def show_versions(models, get_latest_versions):
    df = mk_versions_pandas_df(models, get_latest_versions)
    msg = f"for '{models[0].name}' model" if len(models) == 1 else "for all models"
    which = "Latest" if get_latest_versions else "All"
    print(f"\n{which} {df.shape[0]} versions {msg}")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


def run(model, view, max_results):
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
