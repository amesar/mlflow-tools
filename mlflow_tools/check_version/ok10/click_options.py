
import click

def opt_download_dir(function):
    function = click.option("--download-dir",
        help="Download artifact scratch directory",
        type=str,
        required=False
    )(function)
    return function

def opt_report_file(function):
    function = click.option("--report-file",
        help="Output report file",
        type=str,
        required=False
    )(function)
    return function
