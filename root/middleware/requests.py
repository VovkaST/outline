import logging

logger = logging.getLogger("middleware.requests")


async def request(request, call_next):
    """
    Middleware for request logging
    """
    logger.info(f"Request: {request.method} {request.url}")
    body = await request.body()
    logger.debug(f"Request: {request.method} {request.url}. Body: {body.decode()}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response
