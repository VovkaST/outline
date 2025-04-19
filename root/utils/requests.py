import logging

import aiohttp
from aiohttp import hdrs

logger = logging.getLogger("HTTPClient")


class LoggingClientSession(aiohttp.ClientSession):
    async def _request(self, method, url, **kwargs):
        logger.debug("Starting request <%s %r>", method, self._build_url(url))
        response = await super()._request(method, url, **kwargs)
        data = ""
        content_type = response.headers[hdrs.CONTENT_TYPE]
        if "application/json" in content_type:
            data = await response.json()
        elif "text/xml" in content_type:
            data = await response.text()
        logger.info(f"Request <{method} {response.real_url}> finished: {response.status} {response.reason}")
        logger.debug(f"Request <{method} {response.real_url}> finished: {response.status} {response.reason} {data}")
        return response
