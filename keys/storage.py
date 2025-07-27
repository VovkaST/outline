from root.config import settings
from root.media_storage import LocalStorage


class KeysStorage(LocalStorage):
    def make_name(self, guid: str) -> str:
        return f"{guid}.txt"

    def get(self, name: str) -> str:
        return super().get(name=self.make_name(name))


keys_storage = KeysStorage(settings.MEDIA_DIR / "keys")
