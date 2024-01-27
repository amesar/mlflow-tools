import time
import json
import statistics


def read_data(data_path, num_records):
    with open(data_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    columns = lines[0].split(',')[:-1] # remove label column 'quality'
    columns = [ c.replace('"','') for c in columns]
    print("Columns:",columns)
    lines = lines[1:]
    if num_records:
        lines = lines[:num_records]
    num_records = len(lines)
    print("#Records:",num_records)

    records = []
    for line in lines:
        toks = line.strip().split(',')[:-1]
        r = [float(t) for t in toks ]
        dct = { "columns" : columns, "data" : [r] }
        records.append(dct)

    return records


def show(output_file_base, uri, durations, num_iters, num_records, num_threads=None):
    duration = sum(durations)
    _mean = statistics.mean(durations)
    stdev = statistics.stdev(durations)
    rsd = stdev / _mean * 100 # relative stdev

    stdev = round(stdev,3)
    rsd = round(rsd,2)
    _mean = round(_mean,3)
    duration = round(duration,3)
    _max = round(max(durations),3)
    _min = round(min(durations),3)
    num_requests = len(durations)

    print("Results (seconds):")
    print("  mean:      ", fmt(_mean))
    print("  max:       ", fmt(_max))
    print("  min:       ", fmt(_min))
    print("  requests:  ", num_requests)
    print("  records:   ", num_records)
    print("  iterations:", num_iters)

    if output_file_base:
        now = time.time()
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(now))
        dct = {
          "timestamp": ts,
          "uri": uri,
          "mean": _mean,
          "max": _max,
          "min": _min,
          "std": stdev,
          "rsd": rsd,
          "total": duration,
          "requests": num_requests,
          "records": num_records,
          "iterations": num_iters
        }
        if num_threads:
            dct["threads"] = num_threads
        ts = time.strftime("%Y_%m_%d_%H%M%S", time.gmtime(now))
        path = f"{output_file_base}_{ts}.json"
        #path = f"{output_file_base}.json"
        print("Output file:",path)
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(dct,indent=2)+"\n")


def fmt(x, prec=3):
    y = round(x,prec)
    return str(y).ljust(5, '0')
