import click
from . common import show
from . data_loader import DataLoader
from . client import Client


def run(uri, token, data_path, output_file_base, log_mod, num_requests, add_timestamp_to_output_file, client_request_id):
    data_loader = DataLoader(data_path, num_requests)
    client = Client(uri, token)
    records = [ record for record in data_loader ]
    for j, record in enumerate(records):
        data = data_loader.mk_request(record, client_request_id)
        duration = client.call(data)
        if j % log_mod == 0:
            print(f"Processing: {j}/{len(records)}: request_duration:{round(duration,3)}")
    show(output_file_base, client, len(records), 
        add_timestamp_to_output_file=add_timestamp_to_output_file, 
        client_request_id=client_request_id)


@click.command()
@click.option("--uri", help="Model serving URI", type=str, required=True)
@click.option("--token", help="Databricks token", type=str, required=True)
@click.option("--data-path", help="path for data to score", type=str, required=True)
@click.option("--num-requests", help="Number of requests", type=int, required=True)
@click.option("--log-mod", help="Log output at this modulo", type=int, default=5)
@click.option("--output-file-base", help="Output file base", type=str, required=True)
@click.option("--add-timestamp-to-output-file", help="Add timestamp to output file name", type=bool, default=False)
@click.option("--client-request-id", help="client_request_id", type=str, required=False)

def main(uri, token, data_path, output_file_base, log_mod, num_requests, add_timestamp_to_output_file, client_request_id):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    run(uri, token, data_path, output_file_base, log_mod, num_requests, add_timestamp_to_output_file, client_request_id)


if __name__ == "__main__":
    main()
