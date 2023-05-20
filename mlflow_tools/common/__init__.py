class MlflowToolsException(Exception):
    def __init__(self, ex, http_status_code = -1):
        super().__init__(ex)
        self.http_status_code = http_status_code

