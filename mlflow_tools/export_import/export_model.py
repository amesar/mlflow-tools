"""
Export a registered model and all the experiment runs associated with its latest versions.
"""

import os
import json
import mlflow
from mlflow_tools.common.http_client import HttpClient,MlflowHttpClient
from mlflow_tools.common import filesystem as _filesystem
from mlflow_tools.export_import.export_run import RunExporter
from mlflow_tools.export_import import utils

class ModelExporter():
    def __init__(self, export_metadata_tags=False, notebook_formats=["SOURCE"], filesystem=None):
        self.fs = filesystem or _filesystem.get_filesystem()
        self.client = mlflow.tracking.MlflowClient()
        self.client2 = HttpClient("api/2.0/preview/mlflow")
        self.run_exporter = RunExporter(self.client, export_metadata_tags=export_metadata_tags, notebook_formats=notebook_formats, filesystem=filesystem)

    def export_model(self, output_dir, model_name):
        path = os.path.join(output_dir,"model.json")
        #with open(path, "w") as f:
        model = self.client2.get(f"registered-models/get?name={model_name}")
        for v in model["registered_model"]["latest_versions"]:
            run_id = v["run_id"] 
            opath = os.path.join(output_dir,run_id)
            self.run_exporter.export_run(run_id, opath)
            opath = opath.replace("dbfs:","/dbfs")
            run = self.client.get_run(run_id)
            v["artifact_uri"] = run.info.artifact_uri
        utils.write_json_file(self.fs, path, model)


if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--model", dest="model", help="Registered model name", required=True)
    parser.add_argument("--output_dir", dest="output_dir", help="Output directory", default="out")
    args = parser.parse_args()
    print("Options:")
    for arg in vars(args):
        print("  {}: {}".format(arg,getattr(args, arg)))
    #exporter = ModelExporter(export_metadata_tags=False, notebook_formats=["SOURCE"], filesystem=None) # TODO
    exporter = ModelExporter()
    exporter.export_model(args.output_dir, args.model)
