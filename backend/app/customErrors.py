from fastapi.exceptions import HTTPException
from fastapi import status

class CustomError(HTTPException):
    def __init__(self, detail, status_code):
        super().__init__(
            status_code=status_code,
            detail=detail,
        )
