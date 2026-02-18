from fastapi import Request, status
from fastapi.responses import JSONResponse
from core.exceptions import RetailException, ResourceNotFoundException, BusinessRuleException
from core.logger import logger

async def global_exception_handler(request: Request, exc: Exception):
    """
    Tüm yakalanmayan hataları yakalar, loglar ve standart bir yanıt döner.
    """
    logger.error(f"Global Exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Sunucu hatası. Lütfen daha sonra tekrar deneyin."},
    )

async def retail_exception_handler(request: Request, exc: RetailException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

async def not_found_handler(request: Request, exc: ResourceNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": exc.message},
    )
