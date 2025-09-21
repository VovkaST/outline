__all__ = [
    "planfix_api",
    "payment_api",
    "planfix_webchat",
    "yookassa",
]

from app_server.config import planfix_config, t_bank_config, yookassa_config

from .payment import Payment
from .planfix.client import PlanfixRestAPI, PlanfixWebchatAPI
from .yookassa import YooKassaService

payment_api = None
yookassa = None

planfix_api = PlanfixRestAPI(token=planfix_config.TOKEN)
planfix_webchat = PlanfixWebchatAPI(token=planfix_config.WEBCHAT_TOKEN, provider_id=planfix_config.PROVIDER_ID)

if t_bank_config.TERMINAL_ID and t_bank_config.TERMINAL_PASSWORD:
    payment_api = Payment(
        terminal_id=t_bank_config.TERMINAL_ID,
        terminal_password=t_bank_config.TERMINAL_PASSWORD,
        taxation=t_bank_config.TAXATION,
    )

if yookassa_config.ACCOUNT_ID and yookassa_config.TOKEN:
    yookassa = YooKassaService(yookassa_config.ACCOUNT_ID, yookassa_config.TOKEN)
