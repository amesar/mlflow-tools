"""
List all registered models versions.
"""

import click
from tabulate import tabulate
from mlflow_tools.api import api_factory

pandas_api = api_factory.get_pandas_api()


def to_pandas_dataframe(model_name=None, sort_attribute="name", sort_order="asc", use_by_models=False):
    filter = f"name = '{model_name}'" if model_name else None
    if use_by_models:
        df = pandas_api.search_model_versions_by_models(filter=filter)
    else:
        df = pandas_api.search_model_versions(filter=filter)
    return _to_pandas_dataframe(df, sort_attribute=sort_attribute, sort_order=sort_order)


def _to_pandas_dataframe(df, sort_attribute="name", sort_order="asc"):
    if sort_attribute in df.columns:
        df.sort_values(by=[sort_attribute], inplace=True, ascending=sort_order == "asc")
    return df


def list(model_name, csv_file, sort_attribute="name", sort_order="asc", use_by_models=False):
    df = to_pandas_dataframe(model_name, sort_attribute, sort_order, use_by_models)
    if csv_file:
        with open(csv_file, "w", encoding="utf-8") as f:
            df.to_csv(f, index=False)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


@click.command()
@click.option("--csv-file",
    help="Output CSV file.",
    type=str, 
    required=False,
    show_default=True
)
@click.option("--sort-attr",
    help="Sort by this attibute.",
    type=str, 
    default="name",
    show_default=True
)
@click.option("--sort-order",
    help="Sort order. One of: asc|desc.",
    type=str, 
    default="asc",
    show_default=True
)
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
def main(model, csv_file, sort_attr, sort_order, use_by_models):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    list(model, csv_file, sort_attribute=sort_attr, sort_order=sort_order, use_by_models=use_by_models)


if __name__ == "__main__":
    main()
