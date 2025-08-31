from root.utils.config import BaseAppConfig


class BotAppConfig(BaseAppConfig):
    PREFIX = "BOT"

    TOKEN: str = ""


bot_config = BotAppConfig()
