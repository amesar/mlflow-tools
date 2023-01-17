"""
Dump an experiment in JSON, YAML or text.
"""

import click
import mlflow
from mlflow_tools.tools.utils import format_time
from ..common.http_client import MlflowHttpClient
from ..common import mlflow_utils
from . import dump_dct, show_mlflow_info, write_dct
from . import dump_run, dump_experiment_as_text

http_client = MlflowHttpClient()
mlflow_client = mlflow.tracking.MlflowClient()
max_results = 10000

def dump(exp_id_or_name, 
        artifact_max_level, 
        show_runs=True, 
        show_run_data=False, 
        format="json", 
        output_file=None, 
        explode_json_string=False):
    exp = mlflow_utils.get_experiment(mlflow_client, exp_id_or_name)
    if exp is None:
        raise Exception("Cannot find experiment '{exp_id_or_name}'")
    experiment_id = exp.experiment_id
    dct = {}
    if (format in ["text","txt"]):
        dump_experiment_as_text.dump_experiment(exp_id_or_name, artifact_max_level, show_runs, show_run_data)
    else:
        exp = http_client.get(f"experiments/get?experiment_id={experiment_id}")["experiment"]
        ##if show_run_info or show_run_data:
        if show_runs:
            data = { "experiment_ids" : [experiment_id] , "max_results": max_results}
            runs = http_client.post("runs/search",data)["runs"]
            runs = [dump_run.build_run(run, artifact_max_level, explode_json_string) for run in runs]
            num_artifacts,artifact_bytes = (0,0)
            last_run = 0
            for run in runs:
                if not show_run_data:
                    del run["run"]["data"]
                artifact_bytes += run["summary"]["artifact_bytes"]
                num_artifacts += run["summary"]["artifacts"]
                last_run = max(last_run,int(run["run"]["info"]["end_time"]))
            summary = { 
                "runs": len(runs), "artifacts": num_artifacts, "artifact_bytes": artifact_bytes, 
                "last_run": last_run, "_last_run": format_time(last_run) }
            dct = { "experiment_info": exp, "summary": summary, "runs": runs }
        else:
            dct = exp
        dump_dct(dct, format)
        if output_file:
            write_dct(dct, output_file, format)
    return dct


@click.command()
@click.option("--experiment-id-or-name",
  help="Experiment ID or name",
  type=str,
  required=True
)
@click.option("--artifact-max-level", 
  help="Number of artifact levels to recurse", 
  type=int,
  default=1,
  show_default=True
)
@click.option("--show-runs", 
  help="Show runs",
  type=bool, default=False, 
  show_default=True
)
@click.option("--show-run-data", 
  help="Show run data run if showing runs", 
  type=bool, 
  default=False, 
  show_default=True
)
@click.option("--format", 
  help="Output format: json|yaml|txt", 
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
def main(experiment_id_or_name, artifact_max_level, show_runs, show_run_data, format, explode_json_string, output_file, verbose):
    if verbose:
        show_mlflow_info()
        print("Options:")
        for k,v in locals().items(): print(f"  {k}: {v}")
    dump(experiment_id_or_name, artifact_max_level, 
       show_runs, show_run_data, format, output_file, explode_json_string)


if __name__ == "__main__":
    main()
