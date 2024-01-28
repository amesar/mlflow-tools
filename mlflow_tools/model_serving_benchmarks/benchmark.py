import click
from . common import call, show
from . data_loader import DataLoader


def run(uri, token, data_path, output_file_base, log_mod, num_requests):
    data_loader = DataLoader(data_path, num_requests)
    durations, errors = [], set()
    records = [ record for record in data_loader ]
    for j, record in enumerate(records):
        data = data_loader.mk_request(record)
        duration = call(uri, token, data, errors)
        durations.append(duration)
        if j % log_mod == 0:
            print(f"Processing: {j}/{len(records)}: request_duration:{round(duration,3)}")
    show(output_file_base, uri, durations, len(records), errors)


@click.command()
@click.option("--uri", help="Model serving URI", type=str, required=True)
@click.option("--token", help="Databricks token", type=str, required=True)
@click.option("--data-path", help="path for data to score", type=str, required=True)
@click.option("--num-requests", help="Number of requests", type=int, required=True)
@click.option("--log-mod", help="Log output at this modulo", type=int, default=5)
@click.option("--output-file-base", help="Output file base", type=str, required=True)

def main(uri, token, data_path, output_file_base, log_mod, num_requests):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    run(uri, token, data_path, output_file_base, log_mod, num_requests)


if __name__ == "__main__":
    main()
