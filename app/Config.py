from dotenv import dotenv_values
from pathlib import Path


class Config:
    def __init__(self):
        self.ENV_FILENAME = ".env"
        self.env_file_path = self.project_root_folder / self.ENV_FILENAME
        self.__env = dotenv_values(self.env_file_path)

    @property
    def project_root_folder(self) -> Path:
        return Path(".").absolute()

    @property
    def debug(self) -> bool:
        raw_string = self.__env["DEBUG"]
        print(raw_string)
        return raw_string.lower() == "true"

    @property
    def public_key_path(self) -> Path:
        public_key_raw_path = self.__env["PUBLIC_KEY_PATH"]
        public_key_path = self.project_root_folder / public_key_raw_path
        if Path.exists(public_key_path):
            return public_key_path
        else:
            raise FileNotFoundError("Не найден файл открытого ключа")
