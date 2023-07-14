import click
import mlflow
from mlflow_tools.common.click_options import (
     opt_registered_model,
     opt_model_version,
     opt_tag_key,
     opt_tag_value
)

client = mlflow.MlflowClient()


def set_tag(model_name, version, tag_key, tag_value):
    client.set_model_version_tag(model_name, version, tag_key, tag_value)


@click.command()
@opt_registered_model
@opt_model_version
@opt_tag_key
@opt_tag_value
def main(model, version, tag_key, tag_value):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    set_tag(model, version, tag_key, tag_value)


if __name__ == "__main__":
    main()
