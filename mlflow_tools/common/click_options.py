import click

def opt_output_sort_field(function):
    function = click.option("--sort-field",
        help="Sort by this field.",
        default="name",
        show_default=True
    )(function)
    return function

def opt_output_sort_order(function):
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

# == maybe

def opt_output_csv_file(function):
    function = click.option("--csv-file",
        help="Output CSV file.",
        default="experiments.csv",
        show_default=True
    )(function)
    return function
