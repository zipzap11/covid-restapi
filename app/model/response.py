class Response:
    def __init__(self, ok: bool, data, message: str):
        self.ok = ok
        self.data = data
        self.message = message
