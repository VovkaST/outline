import logging

from root.utils.requests import response_to_str

logger = logging.getLogger("middleware.requests")


async def request(request, call_next):
    """
    Middleware for request logging
    """
    logger.info(f"Request: {request.method} {request.url}")
    body = await request.body()
    logger.debug(f"Request: {request.method} {request.url}. Body: {body.decode()}")
    response = await call_next(request)
    data = await response_to_str(response)
    logger.info(f"Response: {response.status_code}. Body: {data}")
    return response
