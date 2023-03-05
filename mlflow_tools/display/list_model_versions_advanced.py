"""
List all versions of all registered models with info if the version's backing run exists.
"""

import click
import pandas as pd
import mlflow
from tabulate import tabulate
from mlflow_tools.common.mlflow_utils import list_model_versions
from mlflow_tools.common.timestamp_utils import fmt_ts_millis

client = mlflow.client.MlflowClient()

columns = ["Model", "Version", "Stage", "Creation", "Last Updated", "Run ID", "Run stage", "Run exists"]

def mk_versions_pandas_df(models, get_latest_versions=False):
    if isinstance(models,str):
        models = [ client.get_registered_model(models) ]
        df = mk_pandas_version_for_one_model(models[0].name, get_latest_versions)
    elif len(models)==1:
        df = mk_pandas_version_for_one_model(models[0].name, get_latest_versions)
    else:
        df = mk_pandas_version_for_several_models(models, get_latest_versions)
    return df


def mk_pandas_version_for_one_model(model_name, get_latest_versions):
    versions = list_model_versions(client, model_name, get_latest_versions)
    table = [ create_row(vr) for  vr in versions ]
    df = pd.DataFrame(table, columns=columns)
    del df["Model"]
    df = df.sort_values(by=["Version"], ascending=False)
    return df


def mk_pandas_version_for_several_models(models, get_latest_versions):
    if len(models) == 0:
        model_names = []
    elif not isinstance(models[0], str):
        model_names = [ m.name for m in models ]
    else:
        model_names = models
    table = []
    for model_name in model_names:
        versions = list_model_versions(client, model_name, get_latest_versions)
        vtable = [ create_row(vr) for  vr in versions ]
        table += vtable
    df = pd.DataFrame(table, columns=columns)
    df = df.sort_values(by=["Model","Version"], ascending=True)
    return df 


def create_row(vr):
    try:
        run = client.get_run(vr.run_id)
        run_stage = run.info.lifecycle_stage
        run_exists = True
    except mlflow.exceptions.MlflowException:
    #except except mlflow.exceptions.RestException:
        run_stage = None
        run_exists = False
    return [
        vr.name,
        vr.version,
        vr.current_stage,
        fmt_ts_millis(vr.creation_timestamp),
        fmt_ts_millis(vr.last_updated_timestamp),
        vr.run_id,
        run_stage,
        run_exists 
    ]
    

def show_versions(models, get_latest_versions):
    df = mk_versions_pandas_df(models, get_latest_versions)
    msg = f"for '{models[0].name}' model" if len(models) == 1 else "for all models"
    which = "Latest" if get_latest_versions else "All"
    print(f"\n{which} {df.shape[0]} versions {msg}")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


def get_models(model, max_results=1000):
    if model == "all":
        return client.search_registered_models(max_results=max_results)
    else:
        return [ client.get_registered_model(model) ]

def show(model, view, max_results=1000):
    models = get_models(model, max_results)
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
    show(model, view, max_results
)
if __name__ == "__main__":
    main()
