from .base import *

LOGGING["handlers"]["console"]["level"] = "DEBUG"
LOGGING["loggers"]["HTTPClient"]["level"] = "DEBUG"
LOGGING["loggers"]["app_server"]["level"] = "DEBUG"
LOGGING["loggers"]["middleware.requests"]["level"] = "DEBUG"
