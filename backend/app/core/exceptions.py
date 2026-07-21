from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logging import logger

class NeoFactoryException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code

class NotFoundException(NeoFactoryException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)

class ForbiddenException(NeoFactoryException):
    def __init__(self, message: str = "Not enough permissions"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)

class UnauthorizedException(NeoFactoryException):
    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

async def neofactory_exception_handler(request: Request, exc: NeoFactoryException):
    logger.warning(f"Exception: {exc.message} at {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.message, "data": None, "metadata": {}},
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {str(exc)} at {request.url}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "message": "Internal server error", "data": None, "metadata": {}},
    )
