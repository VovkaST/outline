import pathlib


class StorageError(Exception):
    pass


class DoesNotExists(StorageError):
    pass


class LocalStorage:
    encoding = "utf8"

    def __init__(self, root: pathlib.Path = pathlib.Path("/")):
        self.root = root

    def build_absolute(self, path: str) -> pathlib.Path:
        return self.root / path

    def is_absolute(self, path: str) -> bool:
        return str(path).startswith(str(self.root))

    def is_exists(self, path: str) -> bool:
        resource_path = path
        if not self.is_absolute(resource_path):
            resource_path = self.build_absolute(resource_path)
        return resource_path.is_file()

    def save(self, name: str, key: str):
        self.root.mkdir(exist_ok=True)
        file_path = self.build_absolute(name)
        with open(file_path, mode="w", encoding=self.encoding) as file:
            file.write(key)

    def get(self, name: str) -> str:
        resource_path = name
        if not self.is_absolute(resource_path):
            resource_path = self.build_absolute(resource_path)
        if not self.is_exists(resource_path):
            raise DoesNotExists(f"File {resource_path} does not exists")
        return str(resource_path)
