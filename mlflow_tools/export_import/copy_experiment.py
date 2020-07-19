""" 
Copies an experiment from one MLflow server to another.
"""

import click
import mlflow
from mlflow_tools.common import mlflow_utils
from mlflow_tools.export_import import copy_run
from mlflow_tools.export_import.copy_run import RunCopier
from mlflow_tools.export_import import BaseCopier, create_client
from mlflow_tools.export_import import utils 

class ExperimentCopier(BaseCopier):

    def __init__(self, src_client, dst_client, use_src_user_id=False, export_metadata_tags=False, import_metadata_tags=False):
        super().__init__(src_client, dst_client)
        self.export_metadata_tags = export_metadata_tags
        self.run_copier = RunCopier(src_client, dst_client, use_src_user_id, export_metadata_tags)
        self.dst_client = dst_client

    def copy_experiment(self, src_exp_id_or_name, dst_exp_name):
        src_exp = mlflow_utils.get_experiment(self.src_client, src_exp_id_or_name)
        dst_exp = self.get_experiment(self.dst_client, dst_exp_name)
        print("src_experiment_name:",src_exp.name)
        print("src_experiment_id:",src_exp.experiment_id)
        src_infos = self.src_client.list_run_infos(src_exp.experiment_id)
        run_ids_mapping = {}
        for j,info in enumerate(src_infos):
            print(f"Copying run {j+1}/{len(src_infos)}: {info.run_id}")
            dst_run_id, src_parent_run_id = self.run_copier._copy_run(info.run_id, dst_exp.experiment_id)
            run_ids_mapping[info.run_id] = (dst_run_id,src_parent_run_id)
        utils.nested_tags(self.dst_client, run_ids_mapping)

@click.command()
@click.option("--src_uri", help="Source MLflow API URI", required=True, type=str)
@click.option("--dst_uri", help="Destination MLflow API URI", required=True, type=str)
@click.option("--src_experiment", help="Source experiment ID or name", required=True, type=str)
@click.option("--dst_experiment_name", help="Destination experiment name ", required=True, type=str)
@click.option("--use_src_user_id", help="Use source user ID", type=bool, default=False)
@click.option("--export_metadata_tags", help="Export source run metadata tags", type=bool, required=False)
@click.option("--import_metadata_tags", help="Import mlflow_tools tags", type=bool, default=False)

def main(src_uri, dst_uri, src_experiment, dst_experiment_name, use_src_user_id, export_metadata_tags, import_metadata_tags):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    src_client = create_client(src_uri)
    dst_client = create_client(dst_uri)
    print("src_client:",src_client)
    print("dst_client:",dst_client)
    copier = ExperimentCopier(src_client, dst_client, use_src_user_id, export_metadata_tags, import_metadata_tags)
    copier.copy_experiment(src_experiment, dst_experiment_name)

if __name__ == "__main__":
    main()
