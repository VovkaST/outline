from root.utils.config import BaseAppConfig


class BotAppConfig(BaseAppConfig):
    PREFIX = "BOT"

    TOKEN: str = ""
    APP_URL_IOS_EU: str
    APP_URL_IOS_RU: str
    APP_URL_ANDROID: str
    APP_NAME: str

    HOOK_REQUEST_DATA_PREFIX: str = "HOOK_"


class S3Config(BaseAppConfig):
    PREFIX = "S3"

    ACCESS_KEY: str
    SECRET_KEY: str
    BUCKET_NAME: str
    ENDPOINT_URL: str


bot_config = BotAppConfig()
s3_config = S3Config()
