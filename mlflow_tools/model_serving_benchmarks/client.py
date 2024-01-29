import time
import requests

class Client:
    def __init__(self, uri, token):
        self.uri = uri
        self.token = token
        self.durations = []
        self.errors = {}
        self._errors_set = set()
        self.headers = { "Content-Type" : "application/json" , "Authorization": f"Bearer {token}" }

    def call(self, data):
        try:
            start = time.time()
            rsp = requests.post(self.uri, headers=self.headers, json=data, timeout=120) # per mlflow source
            if rsp.status_code < 200 or rsp.status_code > 299:
                print(f"ERROR: status: {rsp.status_code}. {rsp.text}")
                self._add_error(rsp.status_code)
            duration = time.time() - start
            self.durations.append(duration)
        except Exception as ex:
            print(f"ERROR: {ex}")
            self._add_error(str(type(ex)))
        return time.time() - start

    def _add_error(self, error_name):
        self._errors_set.add(error_name)
        count = self.errors.get(error_name)
        if count:
            self.errors[error_name] = count + 1
        else:
            self.errors[error_name] = 1
