import click
import mlflow
from mlflow_tools.common.click_options import (
     opt_registered_model,
     opt_model_version,
     opt_alias
)

client = mlflow.MlflowClient()

def set_alias(model_name, alias, version):
    client.set_registered_model_alias(model_name, alias, version)

@click.command()
@opt_registered_model
@opt_model_version
@opt_alias
def main(model, alias, version):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    set_alias(model, alias, version)


if __name__ == "__main__":
    main()
