"""
Checks if model version runs exist
"""

import click
from dataclasses import dataclass
import pandas as pd
from tabulate import tabulate

import mlflow
from mlflow.exceptions import RestException, MlflowException
from mlflow_export_import.common.click_options import opt_export_latest_versions
from mlflow_export_import.common.timestamp_utils import fmt_ts_millis
from mlflow_export_import.common import utils, model_utils
from mlflow_export_import.bulk import bulk_utils 

_logger = utils.getLogger(__name__)
mlflow_client = mlflow.client.MlflowClient()


@dataclass()
class Stats:
    active: int = 0
    soft_deletes: int = 0
    hard_deletes: int = 0
    other: int = 0
    total: int = 0
    def add(self, stats):
        self.active += stats.active
        self.soft_deletes += stats.soft_deletes
        self.hard_deletes += stats.hard_deletes
        self.other += stats.other
        self.total = self.active + self.soft_deletes + self.hard_deletes + self.other

@dataclass()
class Result:
    df: None
    stats: Stats


def display(model_names, export_latest_versions=False, bail=None, csv_file=None):
    res = mk_pandas_df(model_names, export_latest_versions=export_latest_versions, bail=bail)
    print(tabulate(res.df, headers="keys", tablefmt="psql", showindex=False))
    if csv_file:
        with open(csv_file, "w", encoding="utf-8") as f:
            res.df.to_csv(f, index=False)
    show_stats(res.stats)


def mk_pandas_df(model_names, export_latest_versions=False, bail=None):
    if not model_names in ["*","all"]:
        model_names = model_names.split(",")
    model_names = bulk_utils.get_model_names(mlflow_client, model_names)
    num_models = len(model_names)
    _logger.info(f"Checking {num_models} models")
    stats = Stats()
    data = []
    for idx,model_name in enumerate(model_names):
        sbail = "" if bail is None else f"/{bail}"
        _logger.info(f"{idx+1}{sbail}/{num_models}: Checking model '{model_name}'")
        _stats = build_model(model_name, export_latest_versions, data)
        stats.add(_stats)
        if bail is not None and idx >= bail: 
            break
    if bail is not None:
        print("bailed at model:",bail)

    columns = [ "model","vr_version", "vr_current_stage", "vr_creation_time", "vr_user_id", "run_id", \
        "delete", "run_user_id", "run_start_time", "experiment" ]
    return Result(pd.DataFrame(data, columns = columns), stats)


def build_model(model_name, export_latest_versions, data):
    versions = model_utils.list_model_versions(mlflow_client, model_name, export_latest_versions)
    _logger.info(f"Model '{model_name}' has {len(versions)} versions")
    stats = Stats()
    for vr in versions:
        _logger.debug("version:")
        print(">> version:")
        print(">>   vr.name:",vr.name)
        print(">>   vr.version:",vr.version)
        print(">>   vr.run_id:",vr.run_id)
        print(">>   vr.user_id:",vr.user_id)
        ts = fmt_ts_millis(vr.creation_timestamp)
        msg = { "model": vr.name, "version": vr.version, "run_id": vr.run_id }
        try:
            run = mlflow_client.get_run(vr.run_id)
            exp = mlflow_client.get_experiment(run.info.experiment_id)
            if run.info.lifecycle_stage == "deleted":
                rts = fmt_ts_millis( run.info.start_time)
                #run_user_id = run.info.user_id # deprecated per doc but still exists (?)
                run_user_id = run.data.tags.get("mlflow.user","?")
                data.append([vr.name, vr.version, vr.current_stage, ts, vr.user_id, vr.run_id, "SOFT", run_user_id, rts, exp.name])
                _logger.warning(f"Soft delete: {msg}")
                stats.soft_deletes += 1
            else:
                stats.active += 1
        except RestException as e:
            _logger.warning(f"Hard delete: {msg} EX: {e}")
            data.append([vr.name, vr.version, vr.current_stage, ts, vr.user_id, vr.run_id, "HARD", "", "", ""])
            stats.hard_deletes += 1
        except MlflowException as e:
            _logger.warning(f"Other: {msg} EX: {e}")
            stats.other += 1
            data.append([vr.name, vr.version, vr.current_stage, ts, vr.user_id, vr.run_id, str(e), "", "", ""])
    return stats


def show_stats(stats):
    print("Model Version Run Summary:")
    print(f"  versions: {stats.total}")
    print(f"  active runs: {stats.active}")
    print(f"  soft deletes runs: {stats.soft_deletes}")
    print(f"  hard deletes runs: {stats.hard_deletes}")
    print(f"  other errors: {stats.other}")


@click.command()
@click.option("--models",
    help="Registered model names (comma delimited).  \
        For example, 'model1,model2'. 'all' or '*' will export all models.",
    type=str,
    required=True
)
@opt_export_latest_versions
@click.option("--csv-file",
    help="Output CSV file.",
    type=str,
    required=False,
    show_default=True
)
@click.option("--bail",
    help="Bail out at this model count. Useful to short circuit processing large numbers of models",
    type=int,
    required=False,
    show_default=True
)
def main(models, export_latest_versions, csv_file, bail):
    _logger.info("Options:")
    for k,v in locals().items():
        _logger.info(f"  {k}: {v}")
    display(models, export_latest_versions, bail, csv_file)
    

if __name__ == "__main__":
    main()
