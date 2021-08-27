"""
Dump an experiment in JSON, YAML or text.
"""

import click
import mlflow
from ..common.http_client import MlflowHttpClient
from ..common import mlflow_utils
from . import dump_dct, show_mlflow_info, format_dt
from . import dump_run, dump_experiment_as_text

http_client = MlflowHttpClient()
mlflow_client = mlflow.tracking.MlflowClient()

def _dump_experiment(exp_id_or_name, artifact_max_level, show_info, show_data, format, explode_json_string):
    exp = mlflow_utils.get_experiment(mlflow_client, exp_id_or_name)
    if exp is None:
        raise Exception("Cannot find experiment '{exp_id_or_name}'")
    experiment_id = exp.experiment_id
    #print("experiment_id:",experiment_id)
    if (format in ["text","txt"]):
        dump_experiment_as_text.dump_experiment(exp_id_or_name, artifact_max_level, show_info, show_data)
    else:
        exp = http_client.get(f"experiments/get?experiment_id={experiment_id}")["experiment"]
        if show_info or show_data:
            data = { "experiment_ids" : [experiment_id] , "max_results": 10000}
            runs = http_client.post("runs/search",data)["runs"]
            runs = [dump_run.build_run(run, artifact_max_level, explode_json_string) for run in runs]
            num_artifacts,artifact_bytes = (0,0)
            last_run = 0
            for run in runs:
                artifact_bytes += run["summary"]["artifact_bytes"]
                num_artifacts += run["summary"]["artifacts"]
                last_run = max(last_run,int(run["run"]["info"]["end_time"]))
            summary = { "runs": len(runs), "artifacts": num_artifacts, "artifact_bytes": artifact_bytes, 
               "last_run": last_run, "_last_run": format_dt(last_run) }
            dct = { "experiment_info": exp, "summary": summary, "runs": runs }
            dump_dct(dct, format)

@click.command()
@click.option("--experiment-id-or-name", help="Experiment ID or name", required=True)
@click.option("--artifact-max-level", help="Number of artifact levels to recurse", default=1, type=int)
@click.option("--show-info", help="Show run info", type=bool, default=False, show_default=True)
@click.option("--show-data", help="Show data run info and data", type=bool, default=False, show_default=True)
@click.option("--format", help="Output format: json|yaml|txt", type=str, default="json")
@click.option("--explode-json-string", help="Explode JSON string", type=bool, default=False, show_default=True)
@click.option("--verbose", help="Verbose", type=bool, default=False, show_default=False)
def main(experiment_id_or_name, artifact_max_level, show_info, show_data, format, explode_json_string, verbose):
    if verbose:
        show_mlflow_info()
        print("Options:")
        for k,v in locals().items(): print(f"  {k}: {v}")
    _dump_experiment(experiment_id_or_name, artifact_max_level,show_info, show_data, format, explode_json_string)

if __name__ == "__main__":
    main()
