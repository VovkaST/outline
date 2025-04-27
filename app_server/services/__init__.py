__all__ = [
    "planfix_api",
    "payment_api",
]

from app_server.config import planfix_config, t_bank_config

from .payment import Payment
from .planfix.client import PlanfixRestAPI

planfix_api = PlanfixRestAPI(token=planfix_config.TOKEN)
payment_api = Payment(
    terminal_id=t_bank_config.TERMINAL_ID,
    terminal_password=t_bank_config.TERMINAL_PASSWORD,
    taxation=t_bank_config.TAXATION,
)
