import importlib
import os

DEFAULT_SETTINGS_MODULE = "root.config"


class RootConfig:
    def __init__(self):
        self.SETTINGS_MODULE = os.environ.get("SETTINGS_MODULE", default=DEFAULT_SETTINGS_MODULE)

    def setup(self):
        list_settings = ["MIDDLEWARE"]

        mod = importlib.import_module(self.SETTINGS_MODULE)
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                if setting in list_settings and not isinstance(setting_value, list):
                    raise ValueError(f"Setting {setting} must be a list")

                setattr(self, setting, setting_value)

        for setting in list_settings:
            if not hasattr(self, setting):
                setattr(self, setting, [])

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            "cls": self.__class__.__name__,
            "settings_module": self.SETTINGS_MODULE,
        }


settings = RootConfig()
settings.setup()
