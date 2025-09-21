from pathlib import Path

from root.utils.config import Environ

env = Environ()

ROOT_DIR = Path(__file__).parent.parent

MIDDLEWARE = [
    (
        "starlette.middleware.cors.CORSMiddleware",
        {"allow_credentials": True, "allow_headers": ["*"], "allow_origins": ["*"], "allow_methods": ["*"]},
    ),
    "root.middleware.requests.request",
]

SITE_URL = env.get("SITE_URL", default="http://127.0.0.1:8000")
SITE_URL_PAYMENT = SITE_URL + "/payment"

MEDIA_DIR = env.get("MEDIA_DIR", default="media")
MEDIA_DIR = ROOT_DIR / MEDIA_DIR
MEDIA_DIR.mkdir(exist_ok=True)

# Конфигурация сервера
SERVICE_NAME = env.get("OUTLINE VPN", default="Outline VPN")
SERVER_PORT = env.as_int("SERVER_PORT", default=8000)
SERVER_VERSION = env.get("SERVER_VERSION", default="1.0")
SERVER_DESCRIPTION = env.get("SERVER_DESCRIPTION")
REQUEST_TOKEN = env.get("REQUEST_TOKEN", default="")


# Настройки Т-кассы
TBANK_REST_API_URL = env.get("TBANK_REST_API_URL", default="https://securepay.tinkoff.ru/v2")
TBANK_TERMINAL_ID = env.get("TBANK_TERMINAL_ID")
TBANK_TERMINAL_PASSWORD = env.get("TBANK_TERMINAL_PASSWORD")
TBANK_TAXATION = env.get("TBANK_TAXATION", default="usn_income")
TBANK_USE_SUCCESS_PAYMENT_REDIRECT_URL = env.get("TBANK_USE_SUCCESS_PAYMENT_REDIRECT_URL")
TBANK_USE_FAIL_PAYMENT_REDIRECT_URL = env.get("TBANK_USE_FAIL_PAYMENT_REDIRECT_URL")
DEFAULT_PAYMENT_DESCRIPTION = env.get("DEFAULT_PAYMENT_DESCRIPTION", default="Оплата подписки")
DEFAULT_PAYMENT_DEADLINE = env.as_int("DEFAULT_PAYMENT_DEADLINE", default=30)

# Настройки YooKassa
YOOKASSA_ACCOUNT_ID = env.get("YOOKASSA_ACCOUNT_ID")
YOOKASSA_TOKEN = env.get("YOOKASSA_TOKEN")
YOOKASSA_USE_SUCCESS_PAYMENT_REDIRECT_URL = env.get("YOOKASSA_USE_SUCCESS_PAYMENT_REDIRECT_URL")
YOOKASSA_DEFAULT_CURRENCY = env.get("YOOKASSA_DEFAULT_CURRENCY", default="RUB")


# Настройки Planfix
PLANFIX_XML_API_URL = env.get("PLANFIX_XML_API_URL", default="https://apiru.planfix.ru/xml")
PLANFIX_REST_API_URL = env.get("PLANFIX_REST_API_URL", default="https://aspectgroup.planfix.ru/rest")
PLANFIX_WEBCHAT_API_URL = env.get("PLANFIX_WEBCHAT_API_URL", default="https://aspectgroup.planfix.ru/webchat/api")
PLANFIX_PROVIDER_ID = env.get("PLANFIX_PROVIDER_ID")
PLANFIX_ACCOUNT = env.get("PLANFIX_ACCOUNT")
PLANFIX_TOKEN = env.get("PLANFIX_TOKEN")
PLANFIX_WEBCHAT_TOKEN = env.get("PLANFIX_WEBCHAT_TOKEN")
PLANFIX_API_KEY = env.get("PLANFIX_API_KEY")


# Настройки Telegram-бота
BOT_TOKEN = env.get("BOT_TOKEN")


# Логирование
LOG_DIR = env.get("LOG_DIR", default="logs")
log_dir = Path(LOG_DIR)
log_dir.mkdir(exist_ok=True, parents=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": log_dir / "app.log",
            "maxBytes": 1024 * 1024 * 3,
            "backupCount": 10,
        },
    },
    "loggers": {
        "HTTPClient": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
        "middleware.requests": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
        "app_server": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
        "bot": {
            "level": "INFO",
            "handlers": ["console", "file"],
        },
    },
}
