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

def opt_dump_run(function):
    function = click.option("--dump-run",
        help="Dump run.",
        type=bool,
        default=False,
        show_default=True
    )(function)
    return function

def opt_dump_experiment(function):
    function = click.option("--dump-experiment",
        help="Dump the run's experiment.",
        type=bool,
        default=False,
        show_default=True
    )(function)
    return function

def opt_dump_permissions(function):
    function = click.option("--dump-permissions",
        help="Dump Databricks permissions.",
        type=bool,
        default=False,
        show_default=True
    )(function)
    return function

def opt_artifact_max_level(function):
    function = click.option("--artifact-max-level",
        help="Number of artifact levels to recurse for run artifacts.",
        type=int,
        default=1,
        show_default=True
    )(function)
    return function

def opt_view_type(function):
    function = click.option("--view-type",
        help=f"View type. One of: {VIEW_TYPE_KEYS}.",
        type=str,
        required=False
    )(function)
    return function

def opt_output_csv_file(function):
    function = click.option("--csv-file",
        help="Output CSV file.",
        type=str,
        required=False
    )(function)
    return function

def opt_output_file(function):
    function = click.option("--output-file",
        help="Output file.",
        type=str,
        required=False
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
        default=True,
        show_default=True
    )(function)
    return function

def opt_format(function):
    function = click.option("--format",
        help="Output format. One of: json|yaml.",
        type=str,
        default="json",
        show_default=True
    )(function)
    return function

def opt_explode_json_string(function):
    function = click.option("--explode-json-string",
        help="Explode JSON (or 'sparkDatasourceInfo') string fields as a Python dict or list.",
        type=bool,
        default=True,
        show_default=True
    )(function)
    return function

def opt_show_system_info(function):
    function = click.option("--show-system-info",
        help="Show system info.",
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
