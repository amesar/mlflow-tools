import os
import mlflow

from . import import_run, utils
from . import peek_at_experiment
from .import_run import RunImporter

#from mlflow_tools.export_import import import_run, utils
#from mlflow_tools.export_import.import_run import RunImporter
#from mlflow_tools.export_import import peek_at_experiment

class ExperimentImporter(object):
    def __init__(self, mlflow_client=None, use_src_user_id=False):
        self.client = mlflow_client or mlflow.tracking.MlflowClient()
        self.run_importer = RunImporter(self.client, use_src_user_id)

    def import_experiment(self, exp_name, input):
        if input.endswith(".zip"):
            self.import_experiment_from_zip(exp_name, input)
        else:
            self.import_experiment_from_dir(exp_name, input)

    def import_experiment_from_dir(self, exp_name, exp_dir):
        mlflow.set_experiment(exp_name)
        manifest_path = os.path.join(exp_dir,"manifest.json")
        dct = utils.read_json_file(manifest_path)
        #run_dirs = next(os.walk(exp_dir))[1]
        run_ids = dct['run_ids']
        failed_run_ids = dct['failed_run_ids']
        print("Importing {} runs into experiment '{}' from {}".format(len(run_ids),exp_name,exp_dir),flush=True)
        for src_run_id in run_ids:
            dst_run_id = self.run_importer.import_run(exp_name, os.path.join(exp_dir,src_run_id))
        print("Imported {} runs into experiment '{}' from {}".format(len(run_ids),exp_name,exp_dir),flush=True)
        if len(failed_run_ids) > 0:
            print("Warning: {} failed runs were not imported - see {}".format(len(failed_run_ids),manifest_path))

    def import_experiment_from_zip(self, exp_name, zip_file):
        utils.unzip_directory(zip_file, exp_name, self.import_experiment_from_dir)

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--input", dest="input", help="input path", required=True)
    parser.add_argument("--experiment_name", dest="experiment_name", help="Destination experiment_name", required=True)
    parser.add_argument("--just_peek", dest="just_peek", help="Just display experiment metadata - do not import", default=False, action='store_true')
    parser.add_argument("--use_src_user_id", dest="use_src_user_id", help="Use source user ID", default=False, action='store_true')

    args = parser.parse_args()
    print("Options:")
    for arg in vars(args):
        print("  {}: {}".format(arg,getattr(args, arg)))
    if args.just_peek:
        peek_at_experiment(args.input)
    else:
        importer = ExperimentImporter(None, args.use_src_user_id)
        importer.import_experiment(args.experiment_name, args.input)
