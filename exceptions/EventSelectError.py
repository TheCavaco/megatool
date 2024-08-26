

class EventSelectError(Exception):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        if self.error_code:
            return f"[Error]: {self.args[0]}"
        else:
            return self.args[0]