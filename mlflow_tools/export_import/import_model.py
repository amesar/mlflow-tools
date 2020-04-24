"""
Import a registered model and all the experiment runs associated with its latest versions.
"""

import os
import json
import mlflow
from mlflow_tools.export_import.import_run import RunImporter
from mlflow_tools.export_import import utils
from mlflow_tools.tools import model_utils
from mlflow_tools.common import filesystem as _filesystem

class ModelImporter():
    def __init__(self, filesystem=None):
        self.fs = filesystem or _filesystem.get_filesystem()
        self.client = mlflow.tracking.MlflowClient()
        self.run_importer = RunImporter(self.client)
        #self.run_importer = RunImporter(client, use_src_user_id=False, import_mlflow_tags=False)

    def import_model(self, input_dir, model_name, experiment_name, delete_model):
        path = os.path.join(input_dir,"model.json")
        dct = utils.read_json_file(path)
        dct = dct["registered_model"]

        print("Model to import:")
        print(f"  Name: {dct['name']}")
        print(f"  Description: {dct.get('description','')}")
        print(f"  {len(dct['latest_versions'])} latest versions")

        if delete_model:
            model_utils.delete_model(self.client, model_name)
        self.client.create_registered_model(model_name)
        mlflow.set_experiment(experiment_name)

        print("Importing latest versions:")
        for v in dct["latest_versions"]:
            run_id = v["run_id"]
            source = v["source"]
            current_stage = v["current_stage"]
            artifact_uri = v["artifact_uri"]
            run_dir = os.path.join(input_dir,run_id)
            print(f"  Version {v['version']}:")
            print(f"    current_stage: {v['current_stage']}:")
            print("    Run to import:")
            print("      run_id:", run_id)
            print("      artifact_uri:", artifact_uri)
            print("      source:      ", source)
            model_path = source.replace(artifact_uri+"/","")
            print("      model_path:", model_path)
            print("      run_id:",run_id)
            run_id = self.run_importer.import_run(experiment_name, run_dir)
            run = self.client.get_run(run_id)
            print("    Imported run:")
            print("      run_id:", run_id)
            print("      artifact_uri:", run.info.artifact_uri)
            source = os.path.join(run.info.artifact_uri,model_path)
            print("      source:      ", source)

            version = self.client.create_model_version(model_name, source, run_id)
            model_utils.wait_until_version_is_ready(self.client, model_name, version, sleep_time=2)
            self.client.update_model_version(model_name, version.version, stage=current_stage, description="Imported")

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--input_dir", dest="input_dir", help="Model input directory", required=True)
    parser.add_argument("--model", dest="model", help="New registered model name", required=True)
    parser.add_argument("--experiment_name", dest="experiment_name", help="Experiment name to hold new model runs", required=True)
    parser.add_argument("--delete_model", dest="delete_model", help="Delete new registered model", default=False, action="store_true")
    args = parser.parse_args()
    print("Options:")
    for arg in vars(args):
        print("  {}: {}".format(arg,getattr(args, arg)))
    importer = ModelImporter()
    importer.import_model(args.input_dir, args.model, args.experiment_name, args.delete_model)
