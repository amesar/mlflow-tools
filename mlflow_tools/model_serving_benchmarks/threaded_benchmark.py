import sys
import time
import threading
import click
import pandas as pd
from tabulate import tabulate
from . common import call, show
from . data_loader import DataLoader


class MyThread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)
        self.uri = args[0]
        self.token = args[1]
        self.num_requests = args[2]
        self.data_loader = args[3]
        self.records = args[4]
        self.log_mod = args[5]
        self.thread_idx = args[6]
        self.thread_name = None
        self.mean = -1
        self.max = -1
        self.min = -1
        self.total = 0
        self.durations = []
        self.errors = set()

    def run(self):
        log_filename = f"run_{self.thread_idx}.log"
        with open(log_filename, "w", encoding="utf-8") as f:
            return self._run(f)

    def _run(self, f):
        self.thread_name = threading.current_thread().name
        f.write(f"Requests for thread {self.thread_idx}:\n")
        num_records = len(self.records)

        self.durations, self.errors = [], set()
        for j, record in enumerate(self.records):
            data = self.data_loader.mk_request(record)
            dur = call(self.uri, self.token, data, self.errors)
            if j % self.log_mod == 0:
                f.write(f"{j}/{num_records}: {round(dur,3)}\n")
                ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                sys.stdout.write(f"Processing: {ts} {self.thread_name:8s} rec:{j}/{num_records}: dur:{round(dur,3)}\n")
            self.durations.append(dur)

        self.total = sum(self.durations)
        self.mean = self.total/len(self.durations)
        self.max = max(self.durations)
        self.min = min(self.durations)

        f.write(f"Results (seconds):")
        f.write(f"  mean:    {round(self.mean,3)}\n")
        f.write(f"  max:     {round(self.max,3)}\n")
        f.write(f"  min:     {round(self.min,3)}\n")
        f.write(f"  total:   {round(self.total,3)}\n")
        f.write(f"  records:    {len(self.records)}\n")
        f.write(f"  requests:   {self.num_requests}\n")

    def get_stats(self):
        return self.mean, self.max, self.min, self.total, self.num_requests, self.thread_name


def run(uri, token, data_path, output_file_base, log_mod, num_requests, num_threads):
    data_loader = DataLoader(data_path, num_requests)
    records = [ record for record in data_loader ]
    start_time = time.time()
    threads = []
    for j in range(num_threads):
        thr = MyThread(args=(uri, token, num_requests, data_loader, records, log_mod, j))
        threads.append(thr)
        thr.start()
    print(f"Spawned {num_threads} threads")
    for thr in threads:
        thr.join()
    elapsed_time = time.time() - start_time

    durations = []
    data = []
    errors = set()
    for thr in threads:
        durations += thr.durations
        errors = errors | thr.errors
        _mean,_max,_min, _total, _num_requests, _thr = thr.get_stats()
        data.append([_mean,_max,_min, _total, _num_requests, _thr])
    print("\nSummary")
    df = pd.DataFrame(data, columns = ["Mean", "Max", "Min", "Total", "Requests", "Thread" ])
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    print("elapsed_time:", round(elapsed_time,2))
    print()

    show(output_file_base, uri, durations, len(records), errors, len(threads))


@click.command()
@click.option("--uri", help="Model serving URI", type=str, required=True)
@click.option("--token", help="Databricks token", type=str, required=True)
@click.option("--data-path", help="path for data to score", type=str, required=True)
@click.option("--num-requests", help="Number of requests per each thread", type=int, required=True)
@click.option("--num-threads", help="Number of threads", type=int, required=True)
@click.option("--log-mod", help="Log output at this modulo", type=int, default=5)
@click.option("--output-file-base", help="Output file base", type=str, required=True)

def main(uri, token, data_path, output_file_base, log_mod, num_requests, num_threads):
    print("Options:")
    for k,v in locals().items():
        print(f"  {k}: {v}")
    run(uri, token, data_path, output_file_base, log_mod, num_requests, num_threads)


if __name__ == "__main__":
    main()
