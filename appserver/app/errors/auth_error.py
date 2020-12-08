class AuthException(Exception):
    def __init__(self, status_code, detail):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class MissingTokenError(AuthException):
    def __init__(self):
        message = "Missing token"
        super().__init__(status_code=401, detail=message)


class RevokedIdTokenError(AuthException):
    def __init__(self):
        message = "Token has been revoked"
        super().__init__(status_code=401, detail=message)


class ExpiredIdTokenError(AuthException):
    def __init__(self):
        message = "Token has expired"
        super().__init__(status_code=401, detail=message)


class InvalidIdTokenError(AuthException):
    def __init__(self):
        message = "Invalid token"
        super().__init__(status_code=401, detail=message)
