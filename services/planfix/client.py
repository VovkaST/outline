from aiohttp import BasicAuth, ClientResponse

from app_server.config import planfix_config
from services.base import BaseHTTPService
from services.planfix.api.rest.spec import Contact as RestContact
from services.planfix.api.rest.spec import Task as RestTask
from services.planfix.api.rest.spec import Webchat
from services.planfix.api.xml.functions import Contact, Task


class PlanfixXMLAPI(BaseHTTPService):
    from jinja2 import Environment, PackageLoader

    API_HOST = planfix_config.XML_API_URL
    DEFAULT_HEADERS = {
        "Accept": "application/xml",
        "Content-Type": "application/xml",
    }
    encoding = "UTF-8"

    _templates_env = Environment(loader=PackageLoader("services.planfix.api.xml"))

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


class PlanfixRestAPI(BaseHTTPService):
    urls = {
        "get_task": "task/{task_id}",
        "update_task": "task/{task_id}",
        "task_list": "task/list",
        "add_comment": "task/{task_id}/comments",
        "comments_list": "task/{task_id}/comments/list",
    }
    API_HOST = planfix_config.REST_API_URL

    def __init__(self, token: str, **kwargs):
        self.token = token

        self.task = RestTask(self)
        self.contact = RestContact(self)
        super().__init__(**kwargs)

    def get_session_kwargs(self) -> dict:
        kwargs = super().get_session_kwargs()
        return kwargs | {"headers": {"Authorization": f"Bearer {self.token}"}}

    async def prepare_request(
        self, url_name: str, method: str, json: dict | None = None, data: dict | None = None, **kwargs
    ):
        request_kwargs = await super().prepare_request(url_name, method, json=json or {}, data=data, **kwargs)
        url = request_kwargs["url"]
        if "{task_id}" in url:
            request_kwargs["url"] = url.format(task_id=kwargs["task_id"])
        return request_kwargs


class PlanfixWebchatAPI(BaseHTTPService):
    API_HOST = planfix_config.WEBCHAT_API_URL

    def __init__(self, token: str, provider_id: str, **kwargs):
        self.token = token
        self.provider_id = provider_id
        self.chat = Webchat(self)
        super().__init__(**kwargs)

    def get_session_kwargs(self) -> dict:
        kwargs = super().get_session_kwargs()
        kwargs["raise_for_status"] = True
        return kwargs

    def get_headers(self, url_name: str, method: str) -> dict:
        return {"Content-Type": "application/x-www-form-urlencoded"}

    async def prepare_request(
        self, url_name: str, method: str, json: dict | None = None, data: dict | None = None, **kwargs
    ):
        request_kwargs = await super().prepare_request(url_name, method, json=json, data=data, **kwargs)
        base_message_body = {
            "cmd": url_name,
            "providerId": self.provider_id,
            "planfix_token": self.token + "1",
        }
        request_kwargs["data"] |= base_message_body
        return request_kwargs

    async def handle_response(self, response: ClientResponse) -> str | None:
        return response.reason
