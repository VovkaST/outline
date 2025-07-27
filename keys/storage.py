from root.config import settings
from root.media_storage import LocalStorage


class KeysStorage(LocalStorage):
    def make_name(self, guid: str) -> str:
        return f"{guid}.txt"

    def write(self, file_name: str, key: str):
        file_path = self.build_absolute(file_name)
        with open(file_path, mode="w", encoding="utf8") as file:
            file.write(key)


keys_storage = KeysStorage(settings.MEDIA_DIR / "keys")
