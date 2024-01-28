import csv

class DataLoader:
    def __init__(self, data_path, num_requests):
        self.data_path = data_path
        self.num_requests = num_requests
        self.columns, self.data = self.load(data_path)
        self.counter = 0

    def load(self, path):
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            columns = next(reader)
            data = [ to_float(row) for row in reader ]
        return columns, data

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter >= self.num_requests:
            raise StopIteration
        idx = self.counter % len(self.data)
        self.counter += 1
        return self.data[idx]

    def mk_request(self, data):
        """
        Make a MLflow split-orient request for a list (row).
        """
        return {
            "dataframe_split": {
                "columns": self.columns,
                "data": [ data ]
            }
        }


def to_float(row):
    return [ float(c) for c in row ]
