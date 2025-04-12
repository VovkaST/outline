from root.utils.config import BaseAppConfig


class ServerAppConfig(BaseAppConfig):
    PREFIX = "SERVER"

    PORT: int = 8000
    HOST: str = "127.0.0.1"
    VERSION: str = "1.0"
    DESCRIPTION: str


server_config = ServerAppConfig()
