"""
List all experiments.
"""

import click
from tabulate import tabulate
from mlflow.entities import ViewType
from mlflow_tools.common import pandas_api


def to_pandas_dataframe(sort_attribute="name", sort_order="asc", view_type=ViewType.ACTIVE_ONLY, filter=None, verbose=False):
    df = pandas_api.list_experiments(view_type=view_type, filter=filter)
    if not verbose:
        df = df[["experiment_id","name"]]
    if sort_attribute in df.columns:
        df.sort_values(by=[sort_attribute], inplace=True, ascending=sort_order == "asc")
    return df


def list(csv_file, sort_attribute="name", sort_order="asc", view_type=1, filter=None, verbose=False):
    df = to_pandas_dataframe(sort_attribute, sort_order, view_type, filter, verbose)
    with open(csv_file, "w", encoding="utf-8") as f:
        df.to_csv(f, index=False)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


VIEW_TYPE_KEYS = "|".join(x for x in ViewType._STRING_TO_VIEW.keys())

@click.command()
@click.option("--csv-file",
    help="Output CSV file.",
    default="experiments.csv",
    show_default=True
)
@click.option("--sort-attr",
    help="Sort by this attibute.",
    default="name",
    show_default=True
)
@click.option("--sort-order",
    help="Sort order. One of: asc|desc.",
    default="asc",
    show_default=True
)
@click.option("--view-type", 
    help=f"View type. One of: {VIEW_TYPE_KEYS}.",
    type=str,
    default=ViewType._VIEW_TO_STRING[ViewType.ACTIVE_ONLY],
    show_default=True
)
@click.option("--filter", 
    help=f"Filter",
    type=str,
    required=False
)
@click.option("--verbose",
    help="Verbose.",
    type=bool,
    default=False,
    show_default=True
)
def main(csv_file, sort_attr, sort_order, view_type, filter, verbose):
    print("Options:")
    for k,v in locals().items(): print(f"  {k}: {v}")
    if not ViewType._STRING_TO_VIEW.get(view_type,None):
        print(f"ERROR: Invalid view type '{view_type}'.")
        print(click.get_current_context().get_help())
    else:
        view_type = ViewType.from_string(view_type)
        list(csv_file, sort_attr, sort_order, view_type, filter, verbose)

def print_help():
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()

if __name__ == "__main__":
    main()
