"""
Find artifacts of a run that match a name.
"""

import sys
import os
import click
import mlflow

client = mlflow.client.MlflowClient()


def find_run_model_names(run_id):
    """ 
    Return a list of model artifact directory paths of an MLflow run. 
    Looks for any directory with an 'MLmodel' file and returns its directory.
    """
    matches = find_artifacts(run_id, "", "MLmodel")
    return [ m.replace("/MLmodel","").replace("MLmodel","") for m in matches ]


def find_artifacts(run_id, path, target, max_level=sys.maxsize):
    return _find_artifacts(run_id, path, target, max_level, 0, [])


def _find_artifacts(run_id, path, target, max_level, level, matches):
    if level+1 > max_level: 
        return matches
    artifacts = client.list_artifacts(run_id, path)
    for art in artifacts:
        filename = os.path.basename(art.path)
        if filename == target:
            matches.append(art.path)
        if art.is_dir:
            _find_artifacts(run_id, art.path, target, max_level, level+1, matches)
    return matches


@click.command()
@click.option("--run-id", help="Run ID.", required=True, type=str)
@click.option("--path", help="Relative artifact path.", default="", type=str, show_default=True)
@click.option("--target", help="Target filename to search for.", required=True, type=str)
@click.option("--max-level", help="Number of artifact levels to recurse.", default=sys.maxsize, type=int, show_default=True)

def main(run_id, path, target, max_level): # pragma: no cover
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    matches = find_artifacts(run_id, path, target, max_level)
    print("Matches:")
    for m in matches:
        print(" ",m)


if __name__ == "__main__": 
    main()
