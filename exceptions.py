class DatabaseError(Exception):
    pass

class DbnotFoundException(DatabaseError):
    def __init__(self):
        self.status_code = 404


class ModelNotFoundException(DbnotFoundException):
    def __init__(self, model, model_id):
        self.message = f"{model} {model_id} not found"
        super().__init__()


class ModelInUseError(DatabaseError):
    def __init__(self, model, model_id):
        self.status_code = 422
        self.message = f"{model} {model_id} in use"
        super().__init__()
