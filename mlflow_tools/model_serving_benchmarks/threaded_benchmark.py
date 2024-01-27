import sys
import time
import json
import threading
import requests
import pandas as pd
from tabulate import tabulate
import click
from . common import read_data, show

class MyThread(threading.Thread):
    def __init__(self, args):
        threading.Thread.__init__(self, args=args)
        self.records = args[0]
        self.thr_num = args[1]
        self.num_iters = args[2]
        self.uri = args[3]
        self.log_mod = args[4]
        self.mean = -1
        self.max = -1
        self.min = -1
        self.total = 0
        self.num_requests = 0
        self.durations = []
        self.thread_name = None

    def run(self):
        log_filename = f"run_{self.thr_num}.log"
        with open(log_filename, "w",  encoding="utf-8") as f:
            return self._run(f)

    def _run(self, f):
        headers = { "Content-Type" : "application/json" }
        f.write(f"Requests for thread {self.thr_num}:\n")
        num_records = len(self.records)

        self.durations = []
        for iter in range(0, self.num_iters):
            for j,r in enumerate(self.records):
                self.num_requests += 1
                data = json.dumps(r)
                start = time.time()
                requests.post(self.uri, headers=headers, data=data, timeout=20)
                dur = time.time() - start
                if j % self.log_mod == 0:
                    f.write(f"  {j}/{num_records}: {round(dur,3)}\n")
                    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                    sys.stdout.write(f" {ts} thr_{self.thr_num:03d} iter:{iter+1}/{self.num_iters} rec:{j}/{num_records}: {round(dur,3)}\n")
                self.durations.append(dur)

        self.total = sum(self.durations)
        self.mean = self.total/len(self.durations)
        self.max = max(self.durations)
        self.min = min(self.durations)
        self.thread_name = threading.current_thread().name

        f.write(f"Results (seconds):")
        f.write(f"  mean:    {round(self.mean,3)}\n")
        f.write(f"  max:     {round(self.max,3)}\n")
        f.write(f"  min:     {round(self.min,3)}\n")
        f.write(f"  total:   {round(self.total,3)}\n")
        f.write(f"  records:    {len(self.records)}\n")
        f.write(f"  requests:   {self.num_requests}\n")
        f.write(f"  iterations: {self.num_iters}\n")

    def get_stats(self):
        return self.mean, self.max, self.min, self.total, self.num_requests, self.thread_name



def run(uri, data_path, output_file_base, log_mod, num_records, num_threads, num_iters):
    records = read_data(data_path, num_records)
    num_records = len(records)

    start_time = time.time()
    threads = []
    for j in range(num_threads):
        t = MyThread(args=(records, j, num_iters, uri, log_mod))
        threads.append(t)
        t.start()
    print(f"Spawned {num_threads} threads")
    for t in threads:
        t.join()
    elapsed_time = time.time() - start_time

    durations = []
    data = []
    for thr in threads:
        durations += thr.durations
        _mean,_max,_min, _total, _num_requests, _thr = thr.get_stats()
        data.append([_mean,_max,_min, _total, _num_requests, _thr])
    print("Summary")
    df = pd.DataFrame(data, columns = ["Mean", "Max", "Min", "Total", "Requests", "Thread" ])
    print(tabulate(df, headers="keys", tablefmt="psql", showindex=False))
    print("elapsed_time:", round(elapsed_time,2))

    show(output_file_base, uri, durations, num_iters, num_records, len(threads))


@click.command()
@click.option("--uri", help="Model serving URI", type=str, required=True)
@click.option("--data-path", help="path for data to score", type=str, required=True)
@click.option("--num-records", help="Number of records", type=int, required=True)
@click.option("--num-threads", help="Number of threads", type=int, required=True)
@click.option("--num-iters", help="Number of iterations over data", type=int, required=True)
@click.option("--log-mod", help="Log output at this modulo", type=int, required=True)
@click.option("--output-file-base", help="Output file base", type=str, required=True)

def main(uri, data_path, output_file_base, log_mod, num_records, num_threads, num_iters):
    print("Options:")
    for k,v in locals().items(): 
        print(f"  {k}: {v}")
    run(uri, data_path, output_file_base, log_mod, num_records, num_threads, num_iters)


if __name__ == "__main__":
    main()
