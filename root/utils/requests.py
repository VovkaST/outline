import json
import logging
from contextlib import suppress

import aiohttp
from aiohttp import hdrs
from starlette.responses import JSONResponse

logger = logging.getLogger("HTTPClient")


async def response_to_str(response) -> str | None:
    with suppress(AttributeError):
        if isinstance(response, JSONResponse):
            return response.body.decode()
        if hdrs.CONTENT_TYPE in response.headers:
            content_type = response.headers[hdrs.CONTENT_TYPE]
            if "application/json" in content_type:
                data = await response.json()
                return json.dumps(data, ensure_ascii=True)
            elif "text/xml" in content_type:
                data = await response.text()
                return data.decode()
        return response.reason


class LoggingClientSession(aiohttp.ClientSession):
    async def _request(self, method, url, **kwargs):
        logger.debug("Starting request <%s %r>", method, self._build_url(url))
        json = kwargs.get("json")
        data = kwargs.get("data")
        logger.debug(
            f"Request <{method} {url}> started: {json=}, {data=}",
        )
        response = await super()._request(method, url, **kwargs)
        data = await response_to_str(response)
        logger.info(
            f"Request <{method} {response.real_url}> finished: {response.status} {response.reason}",
        )
        logger.debug(
            f"Request <{method} {response.real_url}> finished: {response.status} {response.reason} {data[:2000]}"
        )
        return response
