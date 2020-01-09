""" 
Exports a run to a directory of zip file.
"""

import os
import shutil
import traceback
import tempfile
import mlflow

from ..common import filesystem as _filesystem
from ..common.http_client import DatabricksHttpClient
from ..common import MlflowToolsException
from ..export_import import utils

print("MLflow Version:", mlflow.version.VERSION)
print("MLflow Tracking URI:", mlflow.get_tracking_uri())

class RunExporter(object):
    def __init__(self, client=None, export_metadata_tags=False, notebook_formats=["SOURCE"], filesystem=None):
        self.client = client or mlflow.tracking.MlflowClient()
        self.dbx_client = DatabricksHttpClient()
        print("Databricks REST client:",self.dbx_client)
        self.fs = filesystem or _filesystem.get_filesystem()
        print("Filesystem:",type(self.fs).__name__)
        self.export_metadata_tags = export_metadata_tags
        self.notebook_formats = notebook_formats

    def export_run(self, run_id, output):
        run = self.client.get_run(run_id)
        if output.endswith(".zip"):
            return self.export_run_to_zip(run, output)
        else:
            self.fs.mkdirs(output)
            return self.export_run_to_dir(run, output)

    def export_run_to_zip(self, run, zip_file):
        temp_dir = tempfile.mkdtemp()
        try:
            res = self.export_run_to_dir(run, temp_dir)
            utils.zip_directory(zip_file, temp_dir)
        finally:
            shutil.rmtree(temp_dir)
            #fs.rm(temp_dir,True) # TODO

    def export_run_to_dir(self, run, run_dir):
        tags =  utils.create_tags_for_metadata(self.client, run, self.export_metadata_tags)
        dct = { "info": utils.strip_underscores(run.info) , 
                "params": run.data.params,
                "metrics": run.data.metrics,
                "tags": tags,
              }
        path = os.path.join(run_dir,"run.json")
        utils.write_json_file(self.fs, path, dct)

        # copy artifacts
        dst_path = os.path.join(run_dir,"artifacts")
        try:
            src_path = self.client.download_artifacts(run.info.run_id,"")
            self.fs.cp(src_path,dst_path,True)
            notebook = tags.get("mlflow.databricks.notebookPath",None)
            if notebook is not None:
                self.export_notebook(run_dir, notebook)
            return True
        except Exception as e: # NOTE: Fails for certain runs in Databricks
            print("ERROR: run_id:",run.info.run_id,"Exception:",e)
            traceback.print_exc()
            return False

    def export_notebook(self, run_dir, notebook):
        for format in self.notebook_formats:
            self.export_notebook_format(run_dir, notebook, format, format.lower())

    def export_notebook_format(self, run_dir, notebook, format, extension):
        resource = f"workspace/export?path={notebook}&direct_download=true&format={format}"
        try:
            rsp = self.dbx_client._get(resource)
            nb_name = "notebook."+extension
            nb_path = os.path.join(run_dir,nb_name)
            utils.write_file(nb_path, rsp.content)
            #self.fs.write(nb_path, rsp.content) # Bombs for DBC because dbutils.fs.put only writes strings!
        except MlflowToolsException as e:
            print(f"WARNING: Cannot save notebook '{notebook}'. {e}")

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--run_id", dest="run_id", help="Source run_id", required=True)
    parser.add_argument("--output", dest="output", help="Output directory or zip file", required=True)
    parser.add_argument("--export_metadata_tags", dest="export_metadata_tags", help="Export source run metadata tags", default=False, action='store_true')
    parser.add_argument("--notebook_formats", dest="notebook_formats", default="SOURCE", help="Notebook formats. Values are SOURCE, HTML, JUPYTER, DBC", required=False)
    args = parser.parse_args()
    print("Options:")
    for arg in vars(args):
        print("  {}: {}".format(arg,getattr(args, arg)))
    exporter = RunExporter(None, args.export_metadata_tags, utils.string_to_list(args.notebook_formats))
    exporter.export_run(args.run_id, args.output)
