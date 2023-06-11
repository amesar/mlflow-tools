"""
Dump an experiment and its runs (optionally) in JSON or YAML.
"""

import click
import mlflow

from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.common.timestamp_utils import fmt_ts_millis
from mlflow_tools.common import mlflow_utils, io_utils, object_utils, permissions_utils
from mlflow_tools.common.http_iterators import SearchRunsIterator
from mlflow_tools.common.click_options import (
    opt_dump_raw,
    opt_artifact_max_level,
    opt_dump_permissions,
    opt_show_tags_as_dict,
    opt_experiment_id_or_name,
    opt_explode_json_string,
    opt_show_system_info,
    opt_format,
    opt_output_file
)
from mlflow_tools.display import dump_run
from mlflow_tools.display.display_utils import dump_finish

http_client = MlflowHttpClient()


def dump(
        experiment_id_or_name,
        dump_raw = False,
        dump_runs = True,
        dump_run_data = False,
        num_runs = None,
        artifact_max_level = 1,
        dump_permissions = False,
        explode_json_string = True,
        show_tags_as_dict = True,
        show_system_info = False,
        format = "json",
        output_file = None,
    ):
    exp = mlflow_utils.get_experiment(http_client, experiment_id_or_name)
    if exp is None:
        raise MlflowToolsException(f"Cannot find experiment '{experiment_id_or_name}'")
    if dump_raw:
        if output_file:
            io_utils.write_file(output_file, exp)
        object_utils.dump_dict_as_json(exp)
        return exp

    exp = exp["experiment"]
    experiment_id = exp["experiment_id"]
    adjust_experiment(exp)

    if dump_runs:
        runs = SearchRunsIterator(http_client, [experiment_id])
        runs = list(runs)
        if num_runs:
            runs = runs[:num_runs]
        runs = [ dump_run.build_run_extended(
                   run = run,
		   artifact_max_level = artifact_max_level,
                   explode_json_string = explode_json_string,
                   show_tags_as_dict = show_tags_as_dict)
            for run in runs ]
        num_artifacts, artifact_bytes = (0, 0)
        last_run = 0
        for run in runs:
            if not dump_run_data:
                del run["run"]["data"]
            artifact_bytes += run["summary"]["artifacts"]["num_bytes"]
            num_artifacts += run["summary"]["artifacts"]["num_artifacts"]
            last_run = max(last_run,int(run["run"]["info"]["end_time"]))
        runs_summary = {
            "num_runs": len(runs),
            "artifacts": num_artifacts,
             "artifact_bytes": artifact_bytes,
            "last_run": last_run,
             "_last_run": fmt_ts_millis(last_run)
        }
        dct = { "experiment": exp, "runs_summary": runs_summary, "runs": runs }
    else:
        dct = { "experiment": exp }

    if dump_permissions:
        permissions_utils.add_experiment_permissions(exp["experiment_id"], dct)

    dct = dump_finish(dct, output_file, format, show_system_info, __file__)
    return dct


def adjust_experiment(exp, show_tags_as_dict=True):
    exp["_last_update_time"] = fmt_ts_millis(exp.get("last_update_time"))
    exp["_creation_time"] = fmt_ts_millis(exp.get("creation_time"))
    exp["_tracking_uri"] = mlflow.get_tracking_uri()
    tags = exp.pop("tags", None)
    if tags:
        if show_tags_as_dict:
            exp["tags"] = mlflow_utils.mk_tags_dict(tags)
        else:
            exp["tags"] = tags


@click.command()
@opt_experiment_id_or_name
@opt_dump_raw
@click.option("--dump-runs",
  help="Show runs",
  type=bool,
  default=False,
  show_default=True
)
@click.option("--dump-run-data",
  help="Show run data run if showing runs",
  type=bool,
  default=False,
  show_default=True
)
@click.option("--num-runs",
  help="Number of runs to dump",
  type=int,
  required=False
)
@opt_artifact_max_level
@opt_dump_permissions
@opt_explode_json_string
@opt_show_tags_as_dict
@opt_show_system_info
@opt_format
@opt_output_file

def main(
        experiment_id_or_name,
        dump_raw,
        artifact_max_level,
        dump_runs,
        dump_run_data,
        num_runs,
        explode_json_string,
        dump_permissions,
        show_tags_as_dict,
        show_system_info,
        format,
        output_file
    ):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    dump(experiment_id_or_name, 
       dump_raw,
       dump_runs, 
       dump_run_data, 
       num_runs,
       artifact_max_level,
       dump_permissions, 
       explode_json_string, 
       show_tags_as_dict,
       show_system_info,
       format, 
       output_file,
   )


if __name__ == "__main__":
    main()
