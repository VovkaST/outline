from root.utils.config import BaseAppConfig


class BotAppConfig(BaseAppConfig):
    PREFIX = "BOT"

    TOKEN: str = ""
    APP_URL_IOS: str = "https://apps.apple.com/us/app/v2raytun/id6476628951?l=ru"
    APP_URL_ANDROID: str = "https://play.google.com/store/apps/details?id=com.v2raytun.android&hl=ru"


bot_config = BotAppConfig()
