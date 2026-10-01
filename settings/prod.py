from .base import *

LOGGING["handlers"]["console"]["level"] = "INFO"
LOGGING["loggers"]["HTTPClient"]["level"] = "INFO"
LOGGING["loggers"]["app_server"]["level"] = "INFO"
LOGGING["loggers"]["middleware.requests"]["level"] = "INFO"
