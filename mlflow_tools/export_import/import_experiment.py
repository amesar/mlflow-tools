import os
import mlflow
import click
from . import import_run, utils
from . import peek_at_experiment
from .import_run import RunImporter

class ExperimentImporter():
    def __init__(self, mlflow_client=None, use_src_user_id=False, import_mlflow_tags=False, import_metadata_tags=False):
        self.client = mlflow_client or mlflow.tracking.MlflowClient()
        self.run_importer = RunImporter(self.client, use_src_user_id, import_mlflow_tags, import_metadata_tags)
        print("MLflowClient:",self.client)

    def import_experiment(self, exp_name, input):
        if input.endswith(".zip"):
            self.import_experiment_from_zip(exp_name, input)
        else:
            self.import_experiment_from_dir(exp_name, input)

    def import_experiment_from_dir(self, exp_name, exp_dir):
        mlflow.set_experiment(exp_name)
        manifest_path = os.path.join(exp_dir,"manifest.json")
        dct = utils.read_json_file(manifest_path)
        run_ids = dct["run_ids"]
        failed_run_ids = dct['failed_run_ids']
        print(f"Importing {len(run_ids)} runs into experiment '{exp_name}' from {exp_dir}")
        run_ids_mapping = {}
        for src_run_id in run_ids:
            dst_run_id, src_parent_run_id = self.run_importer.import_run(exp_name, os.path.join(exp_dir,src_run_id))
            run_ids_mapping[src_run_id] = (dst_run_id,src_parent_run_id)
        print(f"Imported {len(run_ids)} runs into experiment '{exp_name}' from {exp_dir}")
        if len(failed_run_ids) > 0:
            print(f"Warning: {len(failed_run_ids)} failed runs were not imported - see {manifest_path}")
        utils.nested_tags(self.client, run_ids_mapping)

    def import_experiment_from_zip(self, exp_name, zip_file):
        utils.unzip_directory(zip_file, exp_name, self.import_experiment_from_dir)

@click.command()
@click.option("--input", help="Input path - directory or zip file", required=True, type=str)
@click.option("--experiment_name", help="Destination experiment name", required=True, type=str)
@click.option("--just_peek", help="Just display experiment metadata - do not import", type=bool, default=False)
@click.option("--use_src_user_id", help="Use source user ID", type=bool, default=False)
@click.option("--import_mlflow_tags", help="Import mlflow tags", type=bool, default=True)
@click.option("--import_metadata_tags", help="Import mlflow_tools tags", type=bool, default=False)

def main(input, experiment_name, just_peek, use_src_user_id, import_mlflow_tags, import_metadata_tags):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    if just_peek:
        peek_at_experiment(input)
    else:
        importer = ExperimentImporter(None, use_src_user_id, import_mlflow_tags, import_metadata_tags)
        importer.import_experiment(experiment_name, input)

if __name__ == "__main__":
    main()
