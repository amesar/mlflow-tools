""" 
Copies an experiment from one MLflow server to another.
"""

import mlflow
from mlflow_tools.common import mlflow_utils
from mlflow_tools.export_import import copy_run
from mlflow_tools.export_import.copy_run import RunCopier
from mlflow_tools.export_import import BaseCopier, create_client
from mlflow_tools.export_import import utils 

class ExperimentCopier(BaseCopier):

    def __init__(self, src_client, dst_client, export_metadata_tags=False, use_src_user_id=False, import_mlflow_tools_tags=False):
        self.export_metadata_tags = export_metadata_tags
        super().__init__(src_client, dst_client)
        self.run_copier = RunCopier(src_client, dst_client, export_metadata_tags, use_src_user_id, import_mlflow_tools_tags)
        self.dst_client = dst_client

    def copy_experiment(self, src_exp_id_or_name, dst_exp_name):
        src_exp = mlflow_utils.get_experiment(self.src_client, src_exp_id_or_name)
        dst_exp = self.get_experiment(self.dst_client, dst_exp_name)
        print("src_experiment_name:",src_exp.name)
        print("src_experiment_id:",src_exp.experiment_id)
        src_infos = self.src_client.list_run_infos(src_exp.experiment_id)
        run_ids_mapping = {}
        for j,info in enumerate(src_infos):
            print("Copying run {}/{}: {}".format((j+1),len(src_infos),info.run_id))
            dst_run_id, src_parent_run_id = self.run_copier._copy_run(info.run_id, dst_exp.experiment_id)
            run_ids_mapping[info.run_id] = (dst_run_id,src_parent_run_id)
        utils.nested_tags(self.dst_client, run_ids_mapping)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--src_uri", dest="src_uri", help="Source MLFLOW API URL", default=None)
    parser.add_argument("--dst_uri", dest="dst_uri", help="Destination MLFLOW API URL", default=None)
    parser.add_argument("--src_experiment_id_or_name", dest="src_experiment_id_or_name", help="Source experiment ID or name", required=True)
    parser.add_argument("--dst_experiment_name", dest="dst_experiment_name", help="Destination experiment_name", required=True)
    parser.add_argument("--export_metadata_tags", dest="export_metadata_tags", help="Export source run metadata tags", default=False, action='store_true')
    parser.add_argument("--import_mlflow_tools_tags", dest="import_mlflow_tools_tags", help="Import mlflow_tools tags", default=False, action='store_true')
    parser.add_argument("--use_src_user_id", dest="use_src_user_id", help="Use source user ID", default=False, action='store_true')
    #parser.add_argument("--nested_runs", dest="nested_runs", help="nested_runs", default=False, action='store_true')

    args = parser.parse_args()
    print("Options:")
    for arg in vars(args):
        print("  {}: {}".format(arg,getattr(args, arg)))

    src_client = create_client(args.src_uri)
    dst_client = create_client(args.dst_uri)
    print("src_client:",src_client)
    print("dst_client:",dst_client)
    #copier = ExperimentCopier(src_client, dst_client, args.export_metadata_tags, args.use_src_user_id, args.import_mlflow_tools_tags, args.nested_runs)
    copier = ExperimentCopier(src_client, dst_client, args.export_metadata_tags, args.use_src_user_id, args.import_mlflow_tools_tags)
    copier.copy_experiment(args.src_experiment_id_or_name, args.dst_experiment_name)
