from root.utils.config import BaseAppConfig


class BotAppConfig(BaseAppConfig):
    PREFIX = "BOT"

    TOKEN: str = ""
    APP_URL_IOS: str = "https://apps.apple.com/us/app/happ-proxy-utility/id6504287215"
    APP_URL_ANDROID: str = "https://play.google.com/store/apps/details?id=com.happproxy"

    HOOK_REQUEST_DATA_PREFIX: str = "HOOK_"


bot_config = BotAppConfig()
