from copy import copy

from aiohttp import ClientResponse
from aiohttp.typedefs import Query

from root.utils.requests import LoggingClientSession


class BaseHTTPService:
    urls = {}
    DEFAULT_HEADERS = {
        "Accept": "application/json",
        "Content-type": "application/json",
    }
    API_HOST = ""

    def __init__(self, **kwargs):
        self._api_host = None
        self._session = None

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
        return {"base_url": self.api_host}

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
        **kwargs,
    ) -> dict:
        request_kwargs = await self.prepare_request(url_name, method, json=json, params=params, data=data, **kwargs)
        session = session or self.session
        request_method = getattr(session, method)
        async with request_method(**request_kwargs) as response:
            return await self.handle_response(response)
