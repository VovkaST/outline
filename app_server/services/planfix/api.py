from aiohttp import BasicAuth, ClientResponse
from jinja2 import Environment, PackageLoader

from app_server.config import planfix_config
from app_server.services.base import BaseHTTPService
from app_server.services.planfix.functions import Contact, Task


class PlanfixAPI(BaseHTTPService):
    API_HOST = planfix_config.API_URL
    DEFAULT_HEADERS = {
        "Accept": "application/xml",
        "Content-Type": "application/xml",
    }
    encoding = "UTF-8"

    _templates_env = Environment(loader=PackageLoader("app_server.services.planfix"))

    def __init__(self, account: str = "", token: str = "", api_key: str = "", **kwargs):
        self.account = account
        self.token = token
        self.api_key = api_key

        self.task = Task(self)
        self.contact = Contact(self)
        super().__init__(**kwargs)

    def get_session_kwargs(self) -> dict:
        kwargs = super().get_session_kwargs()
        return kwargs | {"auth": BasicAuth(self.api_key, self.token)}

    async def prepare_request(self, url_name: str, method: str, json: dict = None, **kwargs) -> dict:
        xml = self.load_template(url_name, **kwargs)

        request_kwargs = {
            "url": "",
            "headers": self.get_headers(url_name, method),
            "data": xml.encode(self.encoding),
        }
        return request_kwargs

    async def handle_response(self, response: ClientResponse):
        return await response.text(encoding=self.encoding)

    def load_template(self, template_name, **kwargs) -> str:
        template = self._templates_env.get_template(template_name)
        return template.render(account=self.account, **kwargs)
