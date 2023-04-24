import click

from mlflow.entities import ViewType
VIEW_TYPE_KEYS = "|".join(x for x in ViewType._STRING_TO_VIEW.keys())

def opt_sort_attr(function):
    function = click.option("--sort-attr",
        help="Sort by this attr.",
        default="name",
        show_default=True
    )(function)
    return function

def opt_sort_order(function):
    function = click.option("--sort-order",
        help="Sort order. One of: asc|desc.",
        default="asc",
        show_default=True
    )(function)
    return function

def opt_show_permissions(function):
    function = click.option("--show-permissions",
        help="Show Databricks permissions.",
        type=bool,
        default=False,
        show_default=True
    )(function)
    return function

def opt_view_type(function):
    function = click.option("--view-type",
        help=f"View type. One of: {VIEW_TYPE_KEYS}.",
        type=str,
        required=False,
        show_default=True
    )(function)
    return function

def opt_output_csv_file(function):
    function = click.option("--csv-file",
        help="Output CSV file.",
        type=str,
        required=False,
        show_default=True
    )(function)
    return function

def opt_experiment_id_or_name(function):
    function = click.option("--experiment-id-or-name",
        help="Experiment ID or name",
        type=str,
        required=True
    )(function)
    return function

def opt_columns(function):
    function = click.option("--columns",
        help="Columns to display (comma delimited).",
        type=str,
        required=False
    )(function)
    return function

def opt_show_tags_as_dict(function):
    function = click.option("--show-tags-as-dict",
        help="Show MLflow tags as a dictionary instead of a list of key/value pairs.",
        type=bool,
        default=False,
        show_default=True
    )(function)
    return function

def opt_show_local_time(function):
    function = click.option("--show-local-time",
        help="Display timestamps as local time (default is UTC).",
        type=bool,
        default=False,
        show_default=True
    )(function)
    return function

def opt_verbose(function):
    function = click.option("--verbose",
        help="Verbose.",
        type=bool,
        default=False,
        show_default=True
    )(function)
    return function
