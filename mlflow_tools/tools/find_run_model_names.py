"""
Find artifacts that match a filename
"""

import click
from . import find_artifacts


@click.command()
@click.option("--run-id", help="Run ID.", required=True, type=str)

def main(run_id):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    print("Matches:")
    for m in find_artifacts.find_run_model_names(run_id):
        print(" ",m)

if __name__ == "__main__": 
    main()
