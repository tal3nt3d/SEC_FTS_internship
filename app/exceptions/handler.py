from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from app.exceptions.errors import AppException

async def validation_exception_handler(_: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content={
            "details": [error["msg"] for error in exc.errors()]
        },
    )

async def app_exception_handler(_: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "details": exc.detail
        },
    )
    
async def integrity_exception_handler(_: Request, exc: IntegrityError):
    orig = str(exc.orig).lower()
    
    if "unique violation" in orig or "duplicate key" in orig:
        import re
        match = re.search(r"key \((\w+)\)=", str(exc.orig))
        field = match.group(1) if match else "field"
        
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"details": f"Resource with this {field} already exists"}
        )
    
    elif "foreign key" in orig:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"details": "Referenced resource does not exist"}
        )
    
    elif "not null" in orig:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"details": "Required field cannot be empty"}
        )
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"details": "Database integrity error"}
    )