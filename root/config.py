import importlib
import os

DEFAULT_SETTINGS_MODULE = "root.config"


class RootConfig:
    def __init__(self):
        self.SETTINGS_MODULE = os.environ.get("SETTINGS_MODULE", default=DEFAULT_SETTINGS_MODULE)

    def setup(self):
        mod = importlib.import_module(self.SETTINGS_MODULE)
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            "cls": self.__class__.__name__,
            "settings_module": self.SETTINGS_MODULE,
        }


settings = RootConfig()
settings.setup()
