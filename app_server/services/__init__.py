__all__ = [
    "planfix_api",
    "payment_api",
]

from app_server.config import planfix_config, t_bank_config

from .payment import Payment
from .planfix.api import PlanfixAPI

planfix_api = PlanfixAPI(account=planfix_config.ACCOUNT, token=planfix_config.TOKEN, api_key=planfix_config.API_KEY)
payment_api = Payment(terminal_id=t_bank_config.TERMINAL_ID, terminal_password=t_bank_config.TERMINAL_PASSWORD)
