import logging

import aiohttp
from aiohttp import hdrs

logger = logging.getLogger("root")


class LoggingClientSession(aiohttp.ClientSession):
    async def _request(self, method, url, **kwargs):
        logger.debug("Starting request <%s %r>", method, self._build_url(url))
        response = await super()._request(method, url, **kwargs)
        data = ""
        if response.headers[hdrs.CONTENT_TYPE] in "application/json":
            data = await response.json()
        elif response.headers[hdrs.CONTENT_TYPE] in "text/xml":
            data = await response.text()
        logger.info(f"Request <{method} {response.real_url}> finished: {response.status} {response.reason} {data}")
        return response
