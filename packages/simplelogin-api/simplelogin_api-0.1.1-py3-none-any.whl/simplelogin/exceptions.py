
class BaseError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f'<{self.__class__.__name__}: {self.msg}>'

    def __repr__(self):
        return self.__str__()

class APIError(BaseError):
    pass

class ValidationError(BaseError):
    pass

class ClientError(BaseError):
    def __init__(self, msg, status_code: int, data):
        super().__init__(msg)
        self.status_code = status_code
        self.data = data
