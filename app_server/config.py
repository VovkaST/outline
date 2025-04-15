from root.utils.config import BaseAppConfig


class ServerAppConfig(BaseAppConfig):
    PREFIX = "SERVER"

    PORT: int = 8000
    HOST: str = "127.0.0.1"
    VERSION: str = "1.0"
    DESCRIPTION: str


class TBankConfig(BaseAppConfig):
    PREFIX = "TBANK"

    REST_API_URL: str
    TERMINAL_ID: str
    TERMINAL_PASSWORD: str


class PlanfixConfig(BaseAppConfig):
    PREFIX = "PLANFIX"

    REST_API_URL: str
    XML_API_URL: str
    ACCOUNT: str
    TOKEN: str
    API_KEY: str


server_config = ServerAppConfig()
t_bank_config = TBankConfig()
planfix_config = PlanfixConfig()
