__all__ = [
    "planfix_api",
    "payment_api",
    "planfix_webchat",
]

from app_server.config import planfix_config, t_bank_config

from .payment import Payment
from .planfix.client import PlanfixRestAPI, PlanfixWebchatAPI

planfix_api = PlanfixRestAPI(token=planfix_config.TOKEN)
planfix_webchat = PlanfixWebchatAPI(token=planfix_config.WEBCHAT_TOKEN, provider_id=planfix_config.PROVIDER_ID)
payment_api = Payment(
    terminal_id=t_bank_config.TERMINAL_ID,
    terminal_password=t_bank_config.TERMINAL_PASSWORD,
    taxation=t_bank_config.TAXATION,
)
