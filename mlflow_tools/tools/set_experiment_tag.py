import click
import mlflow
from mlflow_tools.common import MlflowToolsException
from mlflow_tools.common.click_options import opt_experiment_id_or_name, opt_tag_key, opt_tag_value
from mlflow_tools.common import mlflow_utils

client = mlflow.MlflowClient()


def set_tag(experiment_id_or_name, tag_key, tag_value):
    exp = mlflow_utils.get_experiment(client, experiment_id_or_name)
    if exp is None:
        raise MlflowToolsException(f"Cannot find experiment '{experiment_id_or_name}'")
    client.set_experiment_tag(exp.experiment_id, tag_key, tag_value)
    

@click.command()
@opt_experiment_id_or_name
@opt_tag_key
@opt_tag_value
def main(experiment_id_or_name, tag_key, tag_value):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    set_tag(experiment_id_or_name, tag_key, tag_value)


if __name__ == "__main__":
    main()
