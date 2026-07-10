import time

from fastapi import Request

from app.core.logger import logger


async def log_requests(request: Request, call_next):
    start_time = time.time()

    logger.info(
        "Request Started | %s %s",
        request.method,
        request.url.path,
    )

    response = await call_next(request)

    process_time = round((time.time() - start_time) * 1000, 2)

    logger.info(
        "Request Completed | %s | %s | %sms",
        response.status_code,
        request.url.path,
        process_time,
    )

    return response
