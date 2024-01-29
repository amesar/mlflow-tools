import sys
import time
import threading
import click
import pandas as pd
from tabulate import tabulate
from . common import show
from . data_loader import DataLoader
from . client import Client

class MyThread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)
        self.uri = args[0]
        self.token = args[1]
        self.num_requests = args[2]
        self.data_loader = args[3]
        self.client = args[4]
        self.records = args[5]
        self.log_mod = args[6]
        self.thread_idx = args[7]
        self.client_request_id = args[8]
        self.thread_name = None
        self.mean = -1
        self.max = -1
        self.min = -1
        self.total = 0

    def run(self):
        log_filename = f"run_{self.thread_idx}.log"
        with open(log_filename, "w", encoding="utf-8") as f:
            return self._run(f)

    def _run(self, f):
        self.thread_name = threading.current_thread().name
        f.write(f"Requests for thread {self.thread_idx}:\n")
        num_records = len(self.records)

        for j, record in enumerate(self.records):
            data = self.data_loader.mk_request(record, self.client_request_id)
            dur = self.client.call(data)
            if j % self.log_mod == 0:
                f.write(f"{j}/{num_records}: {round(dur,3)}\n")
                ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                sys.stdout.write(f"Processing: {ts} {self.thread_name:8s} rec:{j}/{num_records}: dur:{round(dur,3)}\n")

        self.total = sum(self.client.durations)
        self.mean = self.total/len(self.client.durations)
        self.max = max(self.client.durations)
        self.min = min(self.client.durations)

        f.write(f"Results (seconds):")
        f.write(f"  mean:     {round(self.mean,3)}\n")
        f.write(f"  max:      {round(self.max,3)}\n")
        f.write(f"  min:      {round(self.min,3)}\n")
        f.write(f"  total:    {round(self.total,3)}\n")
        f.write(f"  records:  {len(self.records)}\n")
        f.write(f"  requests: {self.num_requests}\n")
        f.write(f"  errors:   {self.client.errors}\n")

    def get_stats(self):
        return self.mean, self.max, self.min, self.total, self.num_requests, self.thread_name


def run(uri, token, data_path, output_file_base, log_mod, num_requests, num_threads, 
        add_timestamp_to_output_file, client_request_id
    ):
    data_loader = DataLoader(data_path, num_requests)
    records = [ record for record in data_loader ]
    client = Client(uri, token)
    start_time = time.time()
    threads = []
    for j in range(num_threads):
        thr = MyThread(args=(uri, token, num_requests, data_loader, client, records, log_mod, j, client_request_id))
        threads.append(thr)
        thr.start()
    print(f"Spawned {num_threads} threads")
    for thr in threads:
        thr.join()
    elapsed_time = time.time() - start_time

    durations = []
    data = []
    errors = {}
    for thr in threads:
        durations += thr.client.durations
        _mean,_max,_min, _total, _num_requests, _thr = thr.get_stats()
        data.append([_mean,_max,_min, _total, _num_requests, _thr])
        _merge(errors, thr.client.errors)
    print("\nSummary")
    df = pd.DataFrame(data, columns = ["Mean", "Max", "Min", "Total", "Requests", "Thread" ])
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    print("elapsed_time:", round(elapsed_time,2))

    print()
    show(output_file_base, client, len(records), len(threads), 
        add_timestamp_to_output_file=add_timestamp_to_output_file,
        client_request_id=client_request_id)



def _merge(dct1, dct2):
    keys = dct1.keys() | dct2.keys()
    for k in keys:
        errors1 = dct1.get(k, 0)
        errors2 = dct2.get(k, 0)
        dct1[k] = errors1 + errors2
    return dct1


@click.command()
@click.option("--uri", help="Model serving URI", type=str, required=True)
@click.option("--token", help="Databricks token", type=str, required=True)
@click.option("--data-path", help="path for data to score", type=str, required=True)
@click.option("--num-requests", help="Number of requests per each thread", type=int, required=True)
@click.option("--num-threads", help="Number of threads", type=int, required=True)
@click.option("--log-mod", help="Log output at this modulo", type=int, default=5)
@click.option("--output-file-base", help="Output file base", type=str, required=True)
@click.option("--add-timestamp-to-output-file", help="Add timestamp to output file name", type=bool, default=False)
@click.option("--client-request-id", help="client_request_id", type=str, required=False)

def main(uri, token, data_path, output_file_base, log_mod, num_requests, num_threads, add_timestamp_to_output_file, client_request_id):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    run(uri, token, data_path, output_file_base, log_mod, num_requests, num_threads, add_timestamp_to_output_file, client_request_id)


if __name__ == "__main__":
    main()
