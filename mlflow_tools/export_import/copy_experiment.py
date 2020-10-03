""" 
Copies an experiment from one MLflow server to another.
"""

import click
from mlflow_tools.common import mlflow_utils
from mlflow_tools.export_import.copy_run import RunCopier
from mlflow_tools.export_import import BaseCopier, create_client
from mlflow_tools.export_import import utils, click_doc

class ExperimentCopier(BaseCopier):

    def __init__(self, src_client, dst_client, use_src_user_id=False, export_metadata_tags=False):
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
@click.option("--src-uri", help="Source MLflow API URI.", required=True, type=str)
@click.option("--dst-uri", help="Destination MLflow API URI.", required=True, type=str)
@click.option("--src-experiment", help="Source experiment ID or name.", required=True, type=str)
@click.option("--dst-experiment-name", help="Destination experiment name.", required=True, type=str)
@click.option("--use-src-user-id", help=click_doc.use_src_user_id, type=bool, default=False, show_default=True)
@click.option("--export-metadata-tags", help=click_doc.export_metadata_tags, type=bool, default=False, show_default=True)

def main(src_uri, dst_uri, src_experiment, dst_experiment_name, use_src_user_id, export_metadata_tags):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    src_client = create_client(src_uri)
    dst_client = create_client(dst_uri)
    print("src_client:",src_client)
    print("dst_client:",dst_client)
    copier = ExperimentCopier(src_client, dst_client, use_src_user_id, export_metadata_tags)
    copier.copy_experiment(src_experiment, dst_experiment_name)

if __name__ == "__main__":
    main()
