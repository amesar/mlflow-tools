import time
import json
import requests
import click
from . common import read_data, show

import platform
print("Versions:")
print("  platform:", platform.platform())
print("  python_version:", platform.python_version())

def run(uri, data_path, output_file_base, log_mod, num_records, num_iters):
    records = read_data(data_path, num_records)
    headers = { 'Content-Type' : 'application/json' }

    durations = []
    for _ in range(num_iters):
        num_records = len(records)
        print("Calls:")
        for j,r in enumerate(records):
            data = json.dumps(r)
            start = time.time()
            requests.post(uri, headers=headers, data=data, timeout=20)
            dur = time.time()-start
            if j % log_mod == 0:
                print(f"  {j}/{num_records}: {round(dur,3)}")
            durations.append(dur)
    show(output_file_base, uri, durations, num_iters, len(records))


@click.command()
@click.option("--uri", help="Model serving URI", type=str, required=True)
@click.option("--data-path", help="path for data to score", type=str, required=True)
@click.option("--num-records", help="Number of records", type=int, required=True)
@click.option("--log-mod", help="Log output at this modulo", type=int, required=True)
@click.option("--num-iters", help="Number of iterations over data", type=int, required=True)
@click.option("--output-file-base", help="Output file base", type=str, required=True)
def main(uri, data_path, output_file_base, log_mod, num_records, num_iters):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    run(uri, data_path, output_file_base, log_mod, num_records, num_iters)


if __name__ == "__main__":
    main()
