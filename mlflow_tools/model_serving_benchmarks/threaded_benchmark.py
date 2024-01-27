import sys
import time
import json
import threading
import requests
import click
from . common import read_data

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

    def run(self):
        log_filename = f"run_{self.thr_num}.log"
        with open(log_filename, "w",  encoding="utf-8") as f:
            return self._run(f)

    def _run(self,f):
        headers = { "Content-Type" : "application/json" }
        durations = []
        f.write(f"Requests for thread {self.thr_num}:\n")
        num_records = len(self.records)

        for iter in range(0,self.num_iters):
            for j,r in enumerate(self.records):
                self.num_requests += 1
                data = json.dumps(r)
                start = time.time()
                requests.post(self.uri, headers=headers, data=data, timeout=20)
                dur = time.time()-start
                if j % self.log_mod == 0:
                    f.write(f"  {j}/{num_records}: {round(dur,3)}\n")
                    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(time.time()))
                    sys.stdout.write(f" {ts} thr_{self.thr_num:03d} iter:{iter+1}/{self.num_iters} rec:{j}/{num_records}: {round(dur,3)}\n")
                durations.append(dur)

        self.total = sum(durations)
        self.mean = self.total/len(durations)
        self.max = max(durations)
        self.min = min(durations)

        f.write(f"Results (seconds):")
        f.write(f"  mean:    {round(self.mean,3)}\n")
        f.write(f"  max:     {round(self.max,3)}\n")
        f.write(f"  min:     {round(self.min,3)}\n")
        f.write(f"  total:   {round(self.total,3)}\n")
        f.write(f"  records:    {len(self.records)}\n")
        f.write(f"  requests:   {self.num_requests}\n")
        f.write(f"  iterations: {self.num_iters}\n")

    def get_stats(self):
        return self.mean, self.max, self.min, self.total, self.num_requests

def fmt(x, prec=3):
    y = round(x,prec)
    return str(y).ljust(5, '0')


def run(uri, data_path, output_file_base, log_mod, num_records, num_threads, num_iters):
    records = read_data(data_path, num_records)

    start_time = time.time()
    threads = []
    for j in range(num_threads):
        t = MyThread(args=(records,j, num_iters, uri, log_mod))
        threads.append(t)
        t.start()
    print(f"Spawned {num_threads} threads")
    for t in threads:
        t.join()

    print("Summary")
    print(f"  Thread Mean  Max   Min   Total  Reqs")
    tot_mean = 0 
    tot_max = sys.float_info.min
    tot_min = sys.float_info.max
    tot_total = 0
    for i,t in enumerate(threads):
        _mean,_max,_min, _total, _num_requests = t.get_stats()
        print(f"  {i:6d} {fmt(_mean)} {fmt(_max)} {fmt(_min)} {fmt(_total,1)} {_num_requests}")
        tot_total += _total
        tot_mean += _mean
        tot_max = max(tot_max,_max)
        tot_min = min(tot_min,_min)
    mean = tot_mean / len(threads)
    print(f"  Total  {fmt(mean,4)} {fmt(tot_max)} {fmt(tot_min)}")

    duration = time.time()-start_time
    num_requests = num_iters * len(threads) * len(records)
    mean_thruput = duration/num_requests
    print("Mean:      ", round(mean,4))
    print("Requests:  ", num_requests)
    print("Records:   ", len(records))
    print("Threads:   ", len(threads))
    print("Total time:", round(duration,1))
    print("Mean throughput:", round(mean_thruput,4))

    if output_file_base:
        now = time.time()
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(now))
        dct = {
          "timestamp": ts,
          "uri": uri,
          "mean": mean,
          "max": tot_max,
          "min": tot_min,
          "threads": len(threads),
          "records": len(records),
          "iterations": num_iters,
          "requests": num_requests,
          "duration": duration,
          "mean_thruput": mean_thruput,
        }
        ts = time.strftime("%Y_%m_%d_%H%M%S", time.gmtime(now))
        path = f"{output_file_base}_{ts}.json"
        print("Output file:",path)
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(dct,indent=2)+"\n")


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
