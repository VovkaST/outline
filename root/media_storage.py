import pathlib


class LocalStorage:
    def __init__(self, root_dir: pathlib.Path = pathlib.Path("/")):
        self.root_dir = root_dir
        self.root_dir.mkdir(exist_ok=True)

    def build_absolute(self, path: str) -> pathlib.Path:
        return self.root_dir / path

    def is_exists(self, path: str) -> bool:
        resource_path = self.build_absolute(path)
        return resource_path.is_file()
