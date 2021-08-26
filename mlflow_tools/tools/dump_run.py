"""
Run dump utilities.
"""

import time
import mlflow
from . import format_dt

INDENT = "  "
MAX_LEVEL = 1
client = mlflow.tracking.MlflowClient()
print("MLflow Tracking URI:", mlflow.get_tracking_uri())

def dump_run(run, max_level=1, indent=""):
    dump_run_info(run.info,indent)
    print(indent+"Params:")
    for k,v in sorted(run.data.params.items()):
        print(f"{indent}  {k}: {v}")
    print(indent+"Metrics:")
    for k,v in sorted(run.data.metrics.items()):
        print(f"{indent}  {k}: {v}")
    print(indent+"Tags:")
    for k,v in sorted(run.data.tags.items()):
        print(f"{indent}  {k}: {v}")
    print(f"{indent}Artifacts:")
    num_bytes, num_artifacts = dump_artifacts(run.info.run_id, "", 0, max_level, indent+INDENT)
    print(f"{indent}Total: bytes: {num_bytes} artifacts: {num_artifacts}")
    return run, num_bytes, num_artifacts
        
def dump_run_id(run_id, max_level=1, indent=""):
    run = client.get_run(run_id)
    return dump_run(run,max_level,indent)

def dump_run_info(info, indent=""):
    print(f"{indent}RunInfo:")
    exp = client.get_experiment(info.experiment_id)
    if exp is None:
        print(f"ERROR: Cannot find experiment ID '{info.experiment_id}'")
        return 
    print(f"{indent}  experiment_name: {exp.name}")
    for k,v in sorted(info.__dict__.items()):
        if not k.endswith("_time"):
            print(f"{indent}  {k[1:]}: {v}")
    start = _dump_time(info,'_start_time',indent)
    end = _dump_time(info,'_end_time',indent)
    if start is not None and end is not None:
        dur = float(end - start)/1000
        print(f"{indent}  _duration:  {dur} seconds")

def _dump_time(info, k, indent=""):
    v = info.__dict__.get(k,None)
    if v is None:
        print(f"{indent}  {k[1:] : <11}:{v}")
    else:
        stime = format_dt(v)
        print(f"{indent}  {k[1:] : <11}:{stime}   {v}")
    return v

def dump_artifacts(run_id, path, level, max_level, indent):
    if level+1 > max_level: 
        return 0,0
    artifacts = client.list_artifacts(run_id,path)
    num_bytes, num_artifacts = (0,0)
    for j,art in enumerate(artifacts):
        print(f"{indent}Artifact {j+1}/{len(artifacts)} - level {level}:")
        num_bytes += art.file_size or 0
        print(f"  {indent}path: {art.path}")
        if art.is_dir:
            b,a = dump_artifacts(run_id, art.path, level+1, max_level, indent+INDENT)
            num_bytes += b
            num_artifacts += a
        else:
            print(f"  {indent}bytes: {art.file_size}")
            num_artifacts += 1
    return num_bytes,num_artifacts

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--run_id", dest="run_id", help="Run ID", required=True)
    parser.add_argument("--artifact_max_level", dest="artifact_max_level", help="Number of artifact levels to recurse", required=False, default=1, type=int)
    args = parser.parse_args()
    print("Arguments:")
    for arg in vars(args):
        print(f"  {arg}: {getattr(args, arg)}")
    dump_run_id(args.run_id, args.artifact_max_level)
