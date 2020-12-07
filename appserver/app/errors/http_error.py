from fastapi import HTTPException


class NotFoundError(HTTPException):
    def __init__(self, item):
        message = f"{item} not found"
        super().__init__(status_code=404, detail=message)


class BadRequestError(HTTPException):
    def __init__(self, message):
        super().__init__(status_code=400, detail=message)


class BadGatewayError(HTTPException):
    def __init__(self):
        message = 'Failed to contact external resource'   
        super().__init__(status_code=400, detail=message)