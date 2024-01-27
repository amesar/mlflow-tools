import time
import json
import requests
import statistics
import click
from . common import read_data

import platform
print("Versions:")
print("  platform:", platform.platform())
print("  python_version:", platform.python_version())

def run(uri, data_path, num_records, log_mod, output_file_base, num_iters):
    records = read_data(data_path, num_records)
    headers = { 'Content-Type' : 'application/json' }

    durations = []
    for iter in range(0,num_iters):
        num_records = len(records)
        print("Calls:")
        for j,r in enumerate(records):
            data = json.dumps(r)
            start = time.time()
            requests.post(uri, headers=headers, data=data)
            dur = time.time()-start
            if j % log_mod == 0:
                print(f"  {j}/{num_records}: {round(dur,3)}")
            durations.append(dur)

    total = sum(durations)
    mean = statistics.mean(durations)
    stdev = statistics.stdev(durations)
    rsd = stdev / mean * 100 # relative stdev

    mean = round(mean,3)
    _max = round(max(durations),3)
    _min = round(min(durations),3)
    stdev = round(stdev,3)
    rsd = round(rsd,2)
    total = round(total,3)

    calls = num_iters * len(records)
    print("Results (seconds):")
    print("  mean:   ", round(mean,3))
    print("  max:    ", _max)
    print("  min:    ", _min)
    print("  std:    ", stdev)
    print("  rsd:    ", rsd)
    print("  total:  ", total)
    print("  calls:     ",calls)
    print("  records:   ",len(records))
    print("  iterations:", num_iters)

    if output_file_base:
        now = time.time()
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(now))
        dct = {
          "timestamp": ts,
          "uri": uri,
          "mean": mean,
          "max": _max,
          "min": _min,
          "std": stdev,
          "rsd": rsd,
          "total": total,
          "calls": calls,
          "records": len(records),
          "iterations": num_iters
        }
        ts = time.strftime("%Y-%m-%d_%H%M%S", time.gmtime(now))
        path = f"{output_file_base}_{ts}.json"
        print("Output file:",path)
        with open(path, "w") as f:
            f.write(json.dumps(dct,indent=2)+"\n")


@click.command()
@click.option("--uri", help="Model serving URI", type=str, required=True)
@click.option("--data-path", help="path for data to score", type=str, required=True)
@click.option("--num-records", help="Num of records", type=int, required=True)
@click.option("--log-mod", help="Log output at this modulo", type=int, required=True)
@click.option("--num-iters", help="Number of iterations over data", type=int, required=True)
@click.option("--output-file-base", help="Output file base", type=str, required=True)
def main(uri, data_path, num_records, log_mod, output_file_base, num_iters):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    run(uri, data_path, num_records, log_mod, output_file_base, num_iters)


if __name__ == "__main__":
    main()
