from dotenv import dotenv_values
from pathlib import Path


class ServerConfig:
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
        return raw_string.lower() == "true"

    @property
    def public_key_path(self) -> Path:
        public_key_raw_path = self.__env["PUBLIC_KEY_PATH"]
        public_key_path = self.project_root_folder / public_key_raw_path
        if Path.exists(public_key_path):
            return public_key_path
        else:
            raise FileNotFoundError("Не найден файл открытого ключа")

    @property
    def application_title(self) -> str:
        return self.__env["TITLE"]

    @property
    def application_version(self) -> str:
        return self.__env["VERSION"]

    @property
    def application_mount_path(self) -> str:
        return self.__env["MOUNT_PATH"]

    @property
    def application_allowed_hosts(self) -> list[str]:
        raw_string = self.__env["ALLOWED_HOSTS"]
        return raw_string.replace(" ", "").split(",")

    @property
    def jwt_allowed_issuer_hosts(self) -> list[str]:
        raw_string = self.__env["ALLOWED_ISSUER_HOSTS"]
        return raw_string.replace(" ", "").split(",")
