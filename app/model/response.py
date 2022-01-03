class SuccessResponse:
    def __init__(self, data):
        self.ok = True
        self.data = data
        self.message = "success"
