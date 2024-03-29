import time
import json
import requests
import statistics


def __call(uri, token, data, errors):
    headers = { "Content-Type" : "application/json" , "Authorization": f"Bearer {token}" }
    start = time.time()
    try:
        rsp = requests.post(uri, headers=headers, json=data, timeout=120) # per mlflow source
        if rsp.status_code < 200 or rsp.status_code > 299:
            errors.add(rsp.status_code)
    except Exception as e:
        errors.add(str(type(e)))
    return time.time() - start


def show(output_file_base, caller, num_records, num_threads=None, add_timestamp_to_output_file=False, client_request_id=None):
    num_requests = len(caller.durations)
    duration = sum(caller.durations)
    if num_requests < 2:
        if num_requests == 1:
            _mean = caller.durations[0]
        else:
            _mean = 0
        _max, _min = _mean, _mean
        stdev, rsd = None, None
    else:
        _mean = statistics.mean(caller.durations)
        stdev = statistics.stdev(caller.durations)
        rsd = stdev / _mean * 100 # relative stdev
        stdev = round(stdev,3)
        rsd = round(rsd,2)
        _max = max(caller.durations)
        _min = min(caller.durations)
    _mean = round(_mean,3)
    duration = round(duration, 3)
    _max = round(_max)
    _min = round(_min)

    num_errors = sum(caller.errors.values())

    now = time.time()
    ts = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(now))
    dct = {
      "timestamp": ts,
      "uri": caller.uri,
      "mean": _mean,
      "max": _max,
      "min": _min,
      "std": stdev,
      "rsd": rsd,
      "total": duration,
      "requests": num_requests,
      "records": num_records,
      "num_errors": num_errors,
      "errors": caller.errors,
      "client_request_id": client_request_id
    }
    if num_threads:
        dct["threads"] = num_threads

    if output_file_base:
        if add_timestamp_to_output_file:
            ts = time.strftime("%Y_%m_%d_%H%M%S", time.gmtime(now))
            path = f"{output_file_base}_{ts}.json"
        else:
            path = f"{output_file_base}.json"
        print("Output file:",path)
        with open(path, "w", encoding="utf-8") as f:
            f.write(json.dumps(dct,indent=2)+"\n")

    print("\nResults (seconds):")
    dump_json(dct)


def dump_json(dct, title=None, sort_keys=None, indent=2):
    if title:
        print(f"{title}:")
    return print(json.dumps(dct, sort_keys=sort_keys, indent=indent))
