from root.utils.config import BaseAppConfig


class BotAppConfig(BaseAppConfig):
    PREFIX = "BOT"

    TOKEN: str = ""
    APP_URL_IOS_EU: str
    APP_URL_IOS_RU: str
    APP_URL_ANDROID: str
    APP_NAME: str

    HOOK_REQUEST_DATA_PREFIX: str = "HOOK_"


bot_config = BotAppConfig()
