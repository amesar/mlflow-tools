""" 
Exports an experiment to a directory or zip file.
"""

import os
import mlflow
import shutil
import tempfile
import click

from ..common import filesystem as _filesystem
from ..common import mlflow_utils
from .export_run import RunExporter
from . import utils

class ExperimentExporter():
    def __init__(self, client=None, export_metadata_tags=False, notebook_formats=["SOURCE"], filesystem=None):
        self.client = client or mlflow.tracking.MlflowClient()
        self.export_metadata_tags = export_metadata_tags
        self.notebook_formats = notebook_formats
        self.fs = filesystem or _filesystem.get_filesystem()
        print("Filesystem:",type(self.fs).__name__)
        self.run_exporter = RunExporter(self.client, export_metadata_tags, notebook_formats, self.fs)

    def export_experiment(self, exp_id_or_name, output, export_metadata_tags=False, notebook_formats=["SOURCE"]):
        exp = mlflow_utils.get_experiment(self.client, exp_id_or_name)
        exp_id = exp.experiment_id
        print(f"Exporting experiment '{exp.name}' (ID {exp.experiment_id}) to '{output}'")
        if output.endswith(".zip"):
            self.export_experiment_to_zip(exp_id, output, export_metadata_tags)
        else:
            self.fs.mkdirs(output)
            self.export_experiment_to_dir(exp_id, output)

    def export_experiment_to_dir(self, exp_id, exp_dir):
        exp = self.client.get_experiment(exp_id)
        dct = {"experiment": utils.strip_underscores(exp)}
        infos = self.client.list_run_infos(exp_id)
        dct["export_info"] = { "export_time": utils.get_now_nice(), "num_runs": len(infos) }
        run_ids = []
        failed_run_ids = []
        for j,info in enumerate(infos):
            run_dir = os.path.join(exp_dir, info.run_id)
            print(f"Exporting run {j+1}/{len(infos)}: {info.run_id}")
            res = self.run_exporter.export_run(info.run_id, run_dir)
            if res:
                run_ids.append(info.run_id)
            else:
                failed_run_ids.append(info.run_id)
        dct["run_ids"] = run_ids
        dct["failed_run_ids"] = failed_run_ids
        path = os.path.join(exp_dir,"manifest.json")
        utils.write_json_file(self.fs, path, dct)
        if len(failed_run_ids) == 0:
            print(f"All {len(run_ids)} runs succesfully exported")
        else:
            print(f"{len(run_ids)}/{len(infos)} runs succesfully exported")
            print(f"{len(failed_run_ids)}/{len(infos)} runs failed")

    def export_experiment_to_zip(self, exp_id, zip_file, export_metadata_tags):
        temp_dir = tempfile.mkdtemp()
        try:
            self.export_experiment_to_dir(exp_id, temp_dir)
            utils.zip_directory(zip_file, temp_dir)
        finally:
            shutil.rmtree(temp_dir)

@click.command()
@click.option("--experiment", help="Experiment name or ID", default=None, type=str)
@click.option("--output", help="Output path", required=True)
@click.option("--export-metadata-tags", help="Export source run metadata tags", type=bool, required=False)
@click.option("--notebook-formats", help="Notebook formats. Values are SOURCE, HTML, JUPYTER, DBC", default="SOURCE")

def main(experiment, output, export_metadata_tags, notebook_formats):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    exporter = ExperimentExporter(None, export_metadata_tags, utils.string_to_list(notebook_formats))
    exporter.export_experiment(experiment, output)

if __name__ == "__main__":
    main()
