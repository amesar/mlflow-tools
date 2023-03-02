
"""
Recursively dumps all information about an experiment including all details of its runs and their params, metrics and artifacts.
Note that this can be expensive. Adjust your artifact_max_level.
"""

import mlflow
from ..common import mlflow_utils
from .dump_run_as_text import dump_run_info, dump_run_id

client = mlflow.client.MlflowClient()

def dump_experiment(exp_id_or_name, artifact_max_level, show_info, show_data):
    exp = mlflow_utils.get_experiment(client, exp_id_or_name)
    if exp is None:
        raise Exception("Cannot find experiment '{exp_id_or_name}'")
    exp_id = exp.experiment_id
    print("experiment_id:",exp_id)
    dump_experiment_details(exp)

    if show_info or show_data:
        runs = client.search_runs(exp_id)
        print("  #runs:",len(runs))
        print("Runs:")
        total_bytes = 0
        for j,run in enumerate(runs):
            print(f"  Run {j+1}/{len(runs)}:")
            if show_data:
                _, num_bytes, _ = dump_run_id(run.info.run_id, artifact_max_level, indent="    ")
            else:
                _, num_bytes, _ = dump_run_info(run.info, indent="    ")
            total_bytes += num_bytes
        print("Total experiment bytes:",total_bytes)

def dump_experiment_details(exp):
    print("Experiment Details:")
    for k,v in exp.__dict__.items(): 
        print(f"  {k[1:]}: {v}")
