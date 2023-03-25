"""
Dump an experiment in JSON, YAML or text.
"""

import click
import mlflow
from mlflow_tools.client.http_client import MlflowHttpClient
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.common.timestamp_utils import fmt_ts_millis
from mlflow_tools.common import mlflow_utils
from mlflow_tools.common import permissions_utils
from mlflow_tools.common.click_options import opt_show_permissions, opt_show_tags_as_dict, opt_experiment_id_or_name
from mlflow_tools.display import dump_dct, show_mlflow_info, write_dct
from mlflow_tools.display import dump_run

http_client = MlflowHttpClient()
mlflow_client = mlflow.client.MlflowClient()
max_results = 10000


def dump(
        experiment_id_or_name, 
        artifact_max_level, 
        show_runs = True, 
        show_run_data = False, 
        format = "json", 
        output_file = None, 
        explode_json_string = False,
        show_permissions = False,
        show_tags_as_dict = False
    ):
    exp = mlflow_utils.get_experiment(mlflow_client, experiment_id_or_name)
    if exp is None:
        raise MlflowToolsException(f"Cannot find experiment '{experiment_id_or_name}'")
    experiment_id = exp.experiment_id
    dct = {}
    exp = http_client.get("experiments/get", {"experiment_id": experiment_id}) ["experiment"]
    exp["_last_update_time"] = fmt_ts_millis(exp.get("last_update_time",None))
    exp["_creation_time"] = fmt_ts_millis(exp.get("creation_time",None))
    tags = exp.pop("tags", None)
    if tags:
        if show_tags_as_dict:
            exp["tags"] = mlflow_utils.mk_tags_dict(tags)
        else:
            exp["tags"] = tags 
    if show_runs:
        data = { "experiment_ids" : [experiment_id] , "max_results": max_results}
        runs = http_client.post("runs/search", data)["runs"]
        runs = [ dump_run.build_run(
                run = run, 
		artifact_max_level = artifact_max_level, 
                explode_json_string = explode_json_string, 
                show_tags_as_dict = show_tags_as_dict) 
            for run in runs ]
        num_artifacts,artifact_bytes = (0,0)
        last_run = 0
        for run in runs:
            if not show_run_data:
                del run["run"]["data"]
            artifact_bytes += run["summary"]["artifact_bytes"]
            num_artifacts += run["summary"]["artifacts"]
            last_run = max(last_run,int(run["run"]["info"]["end_time"]))
        runs_summary = { 
            "runs": len(runs), "artifacts": num_artifacts, "artifact_bytes": artifact_bytes, 
            "last_run": last_run, "_last_run": fmt_ts_millis(last_run) }
        dct = { "experiment_info": exp, "runs_summary": runs_summary, "runs": runs }
    else:
        dct = exp
    if show_permissions and mlflow_utils.calling_databricks():
        permissions_utils.add_experiment_permissions(exp["experiment_id"], dct)
    dump_dct(dct, format)
    if output_file:
        write_dct(dct, output_file, format)
    return dct


@click.command()
@opt_experiment_id_or_name
@click.option("--artifact-max-level", 
  help="Number of artifact levels to recurse", 
  type=int,
  default=1,
  show_default=True
)
@click.option("--show-runs", 
  help="Show runs",
  type=bool, 
  default=False, 
  show_default=True
)
@click.option("--show-run-data", 
  help="Show run data run if showing runs", 
  type=bool, 
  default=False, 
  show_default=True
)
@click.option("--format", 
  help="Output format: json|yaml", 
  type=str, 
  default="json",
  show_default=True
)
@click.option("--explode-json-string", 
  help="Explode attributes that are a JSON string", 
  type=bool, 
  default=False, 
  show_default=True
)
@click.option("--output-file",
  help="Output file (extension will be the format)",
  type=str, 
  required=False
)
@click.option("--verbose", 
  help="Verbose", 
  type=bool, 
  default=False, 
  show_default=False
)
@opt_show_permissions
@opt_show_tags_as_dict

def main(
        experiment_id_or_name, 
        artifact_max_level, 
        show_runs, 
        show_run_data, 
        format, 
        explode_json_string, 
        output_file, 
        show_permissions, 
        show_tags_as_dict, 
        verbose
    ):
    if verbose:
        show_mlflow_info()
        print("Options:")
        for k,v in locals().items(): print(f"  {k}: {v}")
    dump(experiment_id_or_name, artifact_max_level, 
       show_runs, show_run_data, format, output_file, 
       explode_json_string, show_permissions, show_tags_as_dict)


if __name__ == "__main__":
    main()
