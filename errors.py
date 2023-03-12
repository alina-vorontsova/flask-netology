

class HttpError(Exception):

    def __init__(self, status_code: int, desctiption: str | dict | list):

        self.status_code = status_code
        self.description = desctiption