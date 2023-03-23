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


def to_pandas_dataframe(view_type=None, filter=None):
    return pandas_api.search_experiments(view_type=view_type, filter=filter)


def list(csv_file, sort_attr="name", sort_order="asc", view_type=1, filter=None):
    df = to_pandas_dataframe(view_type, filter)
    if csv_file:
        with open(csv_file, "w", encoding="utf-8") as f:
            df.to_csv(f, index=False)
    if sort_attr in df.columns:
        df.sort_values(by=[sort_attr], inplace=True, ascending=sort_order == "asc")
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    print(f"Experiment: {df.shape[0]}")


@click.command()
@opt_sort_attr
@opt_sort_order
@opt_view_type
@click.option("--filter", 
    help=f"Filter",
    type=str,
    required=False
)
@opt_output_csv_file

def main(sort_attr, sort_order, view_type, filter, csv_file):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    if view_type:
        view_type = ViewType.from_string(view_type)
    list(csv_file, sort_attr, sort_order, view_type, filter)


if __name__ == "__main__":
    main()
