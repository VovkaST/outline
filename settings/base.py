from root.utils.config import Environ

env = Environ()

SITE_URL = env.get("SITE_URL", default="http://127.0.0.1:8000")
SITE_URL_PAYMENT = SITE_URL + "/payment"

# Конфигурация сервера
SERVICE_NAME = env.get("OUTLINE VPN", default="Outline VPN")
SERVER_PORT = env.as_int("SERVER_PORT", default=8000)
SERVER_VERSION = env.get("SERVER_VERSION", default="1.0")
SERVER_DESCRIPTION = env.get("SERVER_DESCRIPTION")


# Настройки Т-кассы
TBANK_REST_API_URL = env.get("TBANK_REST_API_URL", default="https://securepay.tinkoff.ru/v2")
TBANK_TERMINAL_ID = env.get("TBANK_TERMINAL_ID")
TBANK_TERMINAL_PASSWORD = env.get("TBANK_TERMINAL_PASSWORD")
TBANK_SUCCESS_PAYMENT_REDIRECT_URL = env.get("TBANK_SUCCESS_PAYMENT_REDIRECT_URL", default=SITE_URL)
DEFAULT_PAYMENT_AMOUNT = env.as_int("DEFAULT_PAYMENT_AMOUNT", default=200_00)


# Настройки Planfix
PLANFIX_XML_API_URL = env.get("PLANFIX_XML_API_URL", default="https://apiru.planfix.ru/xml")
PLANFIX_REST_API_URL = env.get("PLANFIX_REST_API_URL", default="https://aspectgroup.planfix.ru/rest")
PLANFIX_ACCOUNT = env.get("PLANFIX_ACCOUNT")
PLANFIX_TOKEN = env.get("PLANFIX_TOKEN")
PLANFIX_API_KEY = env.get("PLANFIX_API_KEY")
