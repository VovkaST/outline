from app_server.dtos import InitWataPaymentDTO
from app_server.utils import apply_task_id_to_redirect_url
from services import wata_config
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
        success_redirect_url = (
            return_url
            if return_url
            else apply_task_id_to_redirect_url(wata_config.USE_SUCCESS_PAYMENT_REDIRECT_URL, task_id)
        )
        payload = {
            "type": "ManyTime",
            "amount": amount / 100,
            "currency": wata_config.DEFAULT_CURRENCY,
            "description": description or task_id,
            "orderId": task_id,
            "successRedirectUrl": success_redirect_url,
            "failRedirectUrl": return_url or wata_config.USE_FAIL_PAYMENT_REDIRECT_URL,
        }
        response = await self.make_request(url_name="links", method="post", json=payload)
        return InitWataPaymentDTO(**response)
