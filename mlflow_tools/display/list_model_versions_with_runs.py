"""
List all versions of all registered models with info if the version's backing run exists.
"""

import click
import pandas as pd
from tabulate import tabulate
import mlflow
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.common import mlflow_utils
from mlflow_tools.common.timestamp_utils import fmt_ts_millis
from mlflow_tools.common.iterators import SearchRegisteredModelsIterator
from mlflow_tools.common.click_options import opt_output_csv_file, \
  opt_columns, opt_sort_attr, opt_sort_order
from mlflow_tools.display.display_utils import process_df

client = mlflow.client.MlflowClient()

all_columns = ["model", "version", "vr_stage", "vr_created", "vr_updated", "run_id", "run_exists", "run_stage", "run_end" ]
debug = False


def to_pandas_dataframe(
        model_names = None, 
        filter = None, 
        get_latest_versions = None
    ):
    if not model_names and not filter:
        raise MlflowToolsException("Either 'model_names' or 'filter' must be specified")
    if model_names and filter:
        raise MlflowToolsException("Both 'model_names' and 'filter' cannot be specified")
    model_names = _adjust_model_names(model_names, filter)
    table = []
    for model_name in model_names:
        versions = mlflow_utils.list_model_versions(client, model_name, get_latest_versions)
        _table = [ _create_row(vr) for  vr in versions ]
        table += _table
    return pd.DataFrame(table, columns=all_columns)


def show(model_names=None, 
        filter = None, 
        get_latest_versions = None, 
        version_stage = None, 
        run_lifecycle_stage = None, 
        columns = None, 
        sort_attr = None,
        sort_order = None,
        csv_file=None
    ):
    df = to_pandas_dataframe(model_names, filter, get_latest_versions, )
    if version_stage:
        df = df.loc[df["vr_stage"].str.casefold() == version_stage.casefold() ]
    if run_lifecycle_stage:
        df = df.loc[df["run_stage"].str.casefold() == run_lifecycle_stage.casefold() ]
    df = process_df(df, columns, sort_attr=sort_attr, sort_order=sort_order, csv_file=csv_file)
    msg = "latest" if get_latest_versions else "all"
    print(f"\n{df.shape[0]} versions - using '{msg}' get mode")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    print(f"\n{df.shape[0]} versions - using '{msg}' get mode")
    if csv_file:
        with open(csv_file, "w", encoding="utf-8") as f:
            df.to_csv(f, index=False)


def _adjust_model_names(model_names, filter):
    if isinstance(model_names, str):
        model_name = model_names
        if model_name in [ "all", "*" ]:
            return [ m.name for m in list(SearchRegisteredModelsIterator(client)) ]
        else:
            return [ model_name ]
    elif filter:
        return [ m.name for m in list(SearchRegisteredModelsIterator(client, filter=filter)) ]
    else:
        return model_names


def _create_row(vr):
    try:
        run = client.get_run(vr.run_id)
        run_exists = True
        run_stage = run.info.lifecycle_stage or "None"
        run_end = fmt_ts_millis(run.info.end_time)
    except mlflow.exceptions.MlflowException as e:
    #except mlflow.exceptions.RestException:
    # RESOURCE_DOES_NOT_EXIST: Node ID 123793393101613 does not exist
        run_exists = False
        run_stage = None
        run_end = None
        if debug:
            run_end = f"{e} - {type(e)}"
    return [
        vr.name,
        vr.version,
        vr.current_stage,
        fmt_ts_millis(vr.creation_timestamp),
        fmt_ts_millis(vr.last_updated_timestamp),
        vr.run_id,
        run_exists,
        run_stage,
        run_end
    ]


@click.command()
@click.option("--model-names", 
  help="Model names (comma delimited)  or 'all' for all models. Mutually exclusive with 'filter' option", 
  type=str,
  required=False
)
@click.option("--filter", 
  help="Standard filter for search_registered_models(). Mutually exclusive with 'model-names' option",
  type=str,
  required=False
)
@click.option("--get-latest-versions", 
  help="Get 'latest' versions. Otherwise get all versions.",
  type=bool,
  default=False,
  show_default=True
)
@click.option("--version-stage", 
  help="Show versions with specified version stage (Production, Staging, Archived).",
  type=str,
  required=False,
  show_default=True
)
@click.option("--run-lifecycle-stage",
  help="Show versions whose run is of specified lifecycle_stage (active, deleted).",
  type=str,
  required=False,
  show_default=True
)
@opt_sort_attr
@opt_sort_order
@opt_columns
@opt_output_csv_file

def main(model_names, filter, get_latest_versions, version_stage, run_lifecycle_stage, 
        sort_attr, sort_order, columns, csv_file
    ):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    if not model_names and not filter:
        raise MlflowToolsException("Either 'model_names' or 'filter' option must be specified")
    if not filter and not model_names in [ "all", "*" ]:
        model_names = model_names.split(",")
    if columns:
        columns = columns.split(",")
    show(model_names, filter, get_latest_versions, version_stage, run_lifecycle_stage, 
        columns, sort_attr, sort_order, csv_file)


if __name__ == "__main__":
    main()
