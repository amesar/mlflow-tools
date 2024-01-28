import time
import json
import requests
import statistics


def call(uri, token, data, errors):
    headers = { "Content-Type" : "application/json" , "Authorization": f"Bearer {token}" }
    start = time.time()
    rsp = requests.post(uri, headers=headers, json=data, timeout=120)
    duration = time.time()-start
    if rsp.status_code < 200 or rsp.status_code > 299:
        errors.add(rsp.status_code)
    return duration


def show(output_file_base, uri, durations, num_records, errors, num_threads=None):
    num_requests = len(durations)
    duration = sum(durations)
    if num_requests < 2:
        _mean = durations[0]
        stdev = None
        rsd = None
    else:
        _mean = statistics.mean(durations)
        stdev = statistics.stdev(durations)
        rsd = stdev / _mean * 100 # relative stdev
        stdev = round(stdev,3)
        rsd = round(rsd,2)
    _mean = round(_mean,3)
    duration = round(duration,3)
    _max = round(max(durations),3)
    _min = round(min(durations),3)

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
      "errors": list(errors)
    }
    if num_threads:
        dct["threads"] = num_threads
    ts = time.strftime("%Y_%m_%d_%H%M%S", time.gmtime(now))
    path = f"{output_file_base}_{ts}.json"
    #path = f"{output_file_base}.json"
    print("Output file:",path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(dct,indent=2)+"\n")

    print("\nResults (seconds):")
    dump_json(dct)

def fmt(x, prec=3):
    y = round(x,prec)
    return str(y).ljust(5, '0')


def dump_json(dct, title=None, sort_keys=None, indent=2):
    if title:
        print(f"{title}:")
    return print(json.dumps(dct, sort_keys=sort_keys, indent=indent))
