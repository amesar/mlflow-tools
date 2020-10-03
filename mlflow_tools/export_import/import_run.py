"""
Imports a run from a directory of zip file.
"""

import os
import time
import click
import mlflow
from mlflow_tools.export_import import utils
from mlflow_tools.export_import import mk_local_path

class RunImporter():
    def __init__(self, mlflow_client=None, use_src_user_id=False, import_mlflow_tags=True, import_metadata_tags=False):
        self.client = mlflow_client or mlflow.tracking.MlflowClient()
        self.use_src_user_id = use_src_user_id
        self.import_mlflow_tags = import_mlflow_tags
        self.import_metadata_tags = import_metadata_tags
        self.in_databricks = "DATABRICKS_RUNTIME_VERSION" in os.environ
        print(f"in_databricks: {self.in_databricks}")
        print(f"importing_into_databricks: {utils.importing_into_databricks()}")

    def import_run(self, exp_name, input):
        print(f"Importing run into experiment '{exp_name}' from '{input}'")
        if input.endswith(".zip"):
            return self.import_run_from_zip(exp_name, input)
        else:
            return self.import_run_from_dir(exp_name, input)

    def import_run_from_zip(self, exp_name, zip_file):
        utils.unzip_directory(zip_file, exp_name, self.import_run_from_dir)
        return "run_id_TODO"

    def import_run_from_dir(self, dst_exp_name, src_run_id):
        mlflow.set_experiment(dst_exp_name)
        dst_exp = self.client.get_experiment_by_name(dst_exp_name)
        #print("Experiment name:",dst_exp_name)
        #print("Experiment ID:",dst_exp.experiment_id)
        src_run_path = os.path.join(src_run_id,"run.json")
        src_run_dct = utils.read_json_file(src_run_path)
        with mlflow.start_run() as run:
            run_id = run.info.run_id
            self.import_run_data(src_run_dct, run_id, src_run_dct["info"]["user_id"])
            path = os.path.join(src_run_id,"artifacts")
            mlflow.log_artifacts(mk_local_path(path))
        return (run_id, src_run_dct["tags"].get(utils.TAG_PARENT_ID,None))

    def dump_tags(self, tags, msg=""):
        print(f"Tags {msg} - {len(tags)}:")
        for t in tags: print(f"  {t.key} - {t.value}")

    def import_run_data(self, run_dct, run_id, src_user_id):
        from mlflow.entities import Metric, Param, RunTag
        now = round(time.time())
        params = [ Param(k,v) for k,v in run_dct["params"].items() ]
        metrics = [ Metric(k,v,now,0) for k,v in run_dct["metrics"].items() ] # TODO: missing timestamp and step semantics?

        tags = run_dct["tags"]
        if not self.import_mlflow_tags: # remove mlflow tags
            tags = { k:v for k,v in tags.items() if not k.startswith(utils.TAG_PREFIX_MLFLOW) }
        if not self.import_metadata_tags: # remove mlflow_tools tags
            tags = { k:v for k,v in tags.items() if not k.startswith(utils.TAG_PREFIX_METADATA) }
        tags = utils.create_mlflow_tags_for_databricks_import(tags) # remove "mlflow" tags that cannot be imported into Databricks

        tags = [ RunTag(k,str(v)) for k,v in tags.items() ]

        self.dump_tags(tags,"1")
        if not self.in_databricks:
            utils.set_dst_user_id(tags, src_user_id, self.use_src_user_id)
        self.dump_tags(tags,"2")
        self.client.log_batch(run_id, metrics, params, tags)

@click.command()
@click.option("--input", help="Input path - directory or zip file", required=True, type=str)
@click.option("--experiment-name", help="Destination experiment name", required=True, type=str)
@click.option("--use-src-user-id", help="Use source user ID", type=bool, default=False)
@click.option("--import-mlflow-tags", help="Import mlflow tags", type=bool, default=True)
@click.option("--import-metadata-tags", help="Import mlflow_tools tags", type=bool, default=False)

def main(input, experiment_name, use_src_user_id, import_mlflow_tags, import_metadata_tags):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    importer = RunImporter(None,use_src_user_id, import_mlflow_tags, import_metadata_tags)
    importer.import_run(experiment_name, input)

if __name__ == "__main__":
    main()
