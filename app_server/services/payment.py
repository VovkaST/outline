import hashlib
from urllib.parse import urljoin

from app_server import dtos
from app_server.config import t_bank_config


def make_token(base_payload: dict) -> str:
    payload = base_payload | {"Password": t_bank_config.TERMINAL_PASSWORD}
    use_keys = [key for key, value in payload.items() if isinstance(value, (str, int, bool)) and key != "Token"]
    pair_values = []
    for key in sorted(use_keys):
        value = payload[key]
        if isinstance(value, bool):
            value = str(value).lower()
        elif isinstance(value, int):
            value = str(value)
        pair_values.append(value)
    pass_str = "".join(pair_values)
    return hashlib.sha256(pass_str.encode("utf-8")).hexdigest()


def init_payment(task_id: str, customer_key: str) -> dtos.InitPaymentResponse:
    endpoint = urljoin(t_bank_config.REST_API_URL, "v2/Init")
    payload = {
        "TerminalKey": t_bank_config.TERMINAL_ID,
        "Amount": 15000,
        "OrderId": task_id,
        "Description": "Оплата подписки",
        "Recurrent": "Y",
        "CustomerKey": customer_key,
    }
    payload["Token"] = make_token(payload)
    headers = {"Content-type": "application/json"}
    response = requests.post(url=endpoint, json=payload, headers=headers).json()
    return dtos.InitPaymentResponse(**response)
