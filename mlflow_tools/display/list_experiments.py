"""
List all experiments.
"""

import click
from tabulate import tabulate
from mlflow.entities import ViewType
from mlflow_tools.api import api_factory
from mlflow_tools.common.click_options import \
    opt_sort_attr, opt_sort_order, opt_view_type, opt_output_csv_file

pandas_api = api_factory.get_pandas_api()


def to_pandas_dataframe(sort_attr="name", sort_order="asc", view_type=ViewType.ACTIVE_ONLY, filter=None, verbose=False):
    df = pandas_api.search_experiments(view_type=view_type, filter=filter)
    if not verbose:
        df = df[["experiment_id","name"]]
    if sort_attr in df.columns:
        df.sort_values(by=[sort_attr], inplace=True, ascending=sort_order == "asc")
    return df


def list(csv_file, sort_attr="name", sort_order="asc", view_type=1, filter=None, verbose=False):
    df = to_pandas_dataframe(sort_attr, sort_order, view_type, filter, verbose)
    if csv_file:
        with open(csv_file, "w", encoding="utf-8") as f:
            df.to_csv(f, index=False)
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))


@click.command()
@opt_sort_attr
@opt_sort_order
@opt_view_type
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
@opt_output_csv_file

def main(sort_attr, sort_order, view_type, filter, csv_file, verbose):
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
