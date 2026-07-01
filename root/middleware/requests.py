import logging

from starlette.responses import FileResponse, StreamingResponse

logger = logging.getLogger("middleware.requests")


async def request(request, call_next):
    """
    Middleware for request logging
    """
    logger.info("Request: %s %s", request.method, request.url)
    if logger.isEnabledFor(logging.DEBUG):
        body = await request.body()
        logger.debug("Request body: %s", body.decode(errors="replace"))
    response = await call_next(request)
    logger.info("Response: %s", response.status_code)
    if (
        logger.isEnabledFor(logging.DEBUG)
        and not isinstance(response, StreamingResponse | FileResponse)
        and hasattr(response, "body")
        and response.body is not None
    ):
        logger.debug("Response body: %s", response.body.decode(errors="replace"))
    return response
