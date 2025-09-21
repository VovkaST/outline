from root.utils.config import BaseAppConfig


class ServerAppConfig(BaseAppConfig):
    PREFIX = "SERVER"

    PORT: int = 8000
    HOST: str = "127.0.0.1"
    VERSION: str = "1.0"
    DESCRIPTION: str
    MEDIA_DIR: str = "media"


class TBankConfig(BaseAppConfig):
    PREFIX = "TBANK"

    REST_API_URL: str
    TERMINAL_ID: str
    TERMINAL_PASSWORD: str
    TAXATION: str
    USE_SUCCESS_PAYMENT_REDIRECT_URL: str
    USE_FAIL_PAYMENT_REDIRECT_URL: str


class YookassaConfig(BaseAppConfig):
    PREFIX = "YOOKASSA"

    ACCOUNT_ID: str
    TOKEN: str
    USE_SUCCESS_PAYMENT_REDIRECT_URL: str
    DEFAULT_CURRENCY: str


class PlanfixConfig(BaseAppConfig):
    PREFIX = "PLANFIX"

    REST_API_URL: str
    WEBCHAT_API_URL: str
    XML_API_URL: str
    ACCOUNT: str
    TOKEN: str
    WEBCHAT_TOKEN: str
    API_KEY: str
    PROVIDER_ID: str


server_config = ServerAppConfig()
t_bank_config = TBankConfig()
planfix_config = PlanfixConfig()
yookassa_config = YookassaConfig()
