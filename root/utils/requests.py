import logging

import aiohttp

logger = logging.getLogger("root")


class LoggingClientSession(aiohttp.ClientSession):
    async def _request(self, method, url, **kwargs):
        logger.debug("Starting request <%s %r>", method, self._build_url(url))
        response = await super()._request(method, url, **kwargs)
        _json = await response.json()
        logger.info(f"Request <{method} {response.real_url}> finished: {response.status} {response.reason} {_json}")
        return response
