import logging
from copy import copy

import aiohttp
from aiohttp import ClientResponse
from aiohttp.typedefs import Query

from root.config import settings
from root.utils.requests import LoggingClientSession

logger = logging.getLogger("HTTPClient")


class BaseHTTPService:
    urls = {}
    DEFAULT_HEADERS = {
        "Accept": "application/json",
        "Content-type": "application/json",
    }
    API_HOST = ""
    _instances: list["BaseHTTPService"] = []

    def __init__(self, **kwargs):
        self._api_host = None
        self._session = None
        BaseHTTPService._instances.append(self)

    @property
    def api_host(self):
        if not self._api_host:
            self._api_host = self.API_HOST + ("/" if not self.API_HOST.endswith("/") else "")
        return self._api_host

    @property
    def session(self) -> LoggingClientSession:
        if not self._session:
            self._session = LoggingClientSession(**self.get_session_kwargs())
        return self._session

    def get_session_kwargs(self) -> dict:
        return {
            "base_url": self.api_host,
            "timeout": aiohttp.ClientTimeout(
                total=settings.HTTP_CLIENT_TIMEOUT_TOTAL,
                connect=settings.HTTP_CLIENT_TIMEOUT_CONNECT,
            ),
            "connector": aiohttp.TCPConnector(
                limit=settings.HTTP_CLIENT_CONNECTOR_LIMIT,
                ttl_dns_cache=settings.HTTP_CLIENT_DNS_CACHE_TTL,
                enable_cleanup_closed=True,
            ),
        }

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
        self._session = None

    @classmethod
    async def close_all(cls) -> None:
        for instance in cls._instances:
            await instance.close()

    def get_headers(self, url_name: str, method: str) -> dict:
        return copy(self.DEFAULT_HEADERS)

    async def prepare_request(
        self, url_name: str, method: str, json: dict | None = None, data: dict | None = None, **kwargs
    ):
        kwargs = {
            "url": self.urls.get(url_name) or "",
            "params": kwargs.get("params") or {},
            "headers": self.get_headers(url_name, method),
        }
        if json:
            kwargs["json"] = json
        if data:
            kwargs["data"] = data
        return kwargs

    async def handle_response(self, response: ClientResponse):
        return await response.json()

    async def make_request(
        self,
        url_name: str,
        method: str,
        json: dict | None = None,
        params: Query = None,
        session=None,
        data: dict | None = None,
        *,
        _retry: bool = False,
        **kwargs,
    ) -> dict:
        """Выполнить HTTP-запрос к внешнему API.

        При сетевых сбоях (ClientConnectorError, ServerDisconnectedError, TimeoutError)
        один раз закрывает сессию, создаёт новую и повторяет запрос.
        Повторный вызов возможен только при _retry=False (не более одной попытки).
        """
        request_kwargs = await self.prepare_request(url_name, method, json=json, params=params, data=data, **kwargs)
        use_session = self.session if _retry else (session or self.session)
        request_method = getattr(use_session, method)
        try:
            async with request_method(**request_kwargs) as response:
                return await self.handle_response(response)
        except (aiohttp.ClientConnectorError, aiohttp.ServerDisconnectedError, TimeoutError) as exc:
            if not _retry:
                logger.warning("HTTP session reset after %s, retrying once: %s", type(exc).__name__, exc)
                await self.close()
                return await self.make_request(
                    url_name,
                    method,
                    json=json,
                    params=params,
                    data=data,
                    _retry=True,
                    **kwargs,
                )
            raise
