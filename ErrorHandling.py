class ErrorHandler:
    def __init__(self):
        self.retry_limit = 3

    def handle_error(self, task):
        retries = 0
        while retries < self.retry_limit:
            try:
                task()
                break
            except Exception as e:
                retries += 1
                if retries == self.retry_limit:
                    print(f"Task failed after {self.retry_limit} retries")
                else:
                    print(f"Retrying task due to error: {e}")
