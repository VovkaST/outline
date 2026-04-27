from app_server.dtos import InitWataPaymentDTO
from services.http_service import BaseHTTPService


class WataService(BaseHTTPService):
    urls = {
        "links": "links",
    }
    API_HOST = "https://api.wata.pro/api/h2h/"

    def __init__(self, token: str, **kwargs):
        super().__init__(**kwargs)
        self.token = token

    def get_headers(self, url_name: str, method: str) -> dict:
        headers = super().get_headers(url_name, method)
        headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def init_payment(
        self,
        task_id: str,
        amount: int,
        description: str = "",
        return_url: str = "",
        **kwargs,
    ):
        payload = {
            "type": "ManyTime",
            "amount": amount / 100,
            "currency": "RUB",
            "description": description or task_id,
            "orderId": task_id,
            "successRedirectUrl": return_url,
            "failRedirectUrl": return_url,
        }
        response = await self.make_request(url_name="links", method="post", json=payload)
        return InitWataPaymentDTO(**response)
