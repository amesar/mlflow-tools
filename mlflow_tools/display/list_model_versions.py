"""
List all registered models versions.
"""

import click
from tabulate import tabulate
from mlflow_tools.common.click_options import opt_sort_attr, opt_sort_order, opt_columns, opt_output_csv_file
from mlflow_tools.api import api_factory
from mlflow_tools.display.display_utils import process_df

pandas_api = api_factory.get_pandas_api()


def to_pandas_dataframe(model_name=None, use_by_models=False):
    filter = f"name = '{model_name}'" if model_name else None
    if use_by_models:
        df = pandas_api.search_model_versions_by_models(filter=filter)
    else:
        df = pandas_api.search_model_versions(filter=filter)
    return df

def list(model_name, columns=None, csv_file=None, sort_attr="name", sort_order="asc", use_by_models=False):
    df = to_pandas_dataframe(model_name, use_by_models)
    df = process_df(df, columns, sort_attr, sort_order, csv_file)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    print(f"Versions: {df.shape[0]}")


@click.command()
@opt_sort_attr
@opt_sort_order
@click.option("--use-by-models", 
    help="Use 'by models' variant to search for versions.", 
    type=bool, 
    required=False
)
@click.option("--model",
    help="Registered model to filter by.",
    type=str, 
    required=False,
    show_default=True
)
@opt_columns
@opt_output_csv_file

def main(model, sort_attr, sort_order, use_by_models, columns, csv_file):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    list(model, 
        sort_attr = sort_attr, 
        sort_order = sort_order,
        use_by_models = use_by_models,
        columns = columns, 
        csv_file = csv_file
    )


if __name__ == "__main__":
    main()
