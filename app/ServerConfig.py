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
        raw_string = self.__env["APP_DEBUG"]
        return raw_string.lower() == "true"

    @property
    def public_key_path(self) -> Path:
        public_key_raw_path = self.__env["JWT_PUBLIC_KEY_PATH"]
        public_key_path = self.project_root_folder / public_key_raw_path
        if Path.exists(public_key_path):
            return public_key_path
        else:
            raise FileNotFoundError("Не найден файл открытого ключа")

    @property
    def application_title(self) -> str:
        return self.__env["APP_TITLE"]

    @property
    def application_version(self) -> str:
        return self.__env["APP_VERSION"]

    @property
    def application_mount_path(self) -> str:
        return self.__env["APP_MOUNT_PATH"]

    @property
    def application_allowed_hosts(self) -> list[str]:
        raw_string = self.__env["APP_ALLOWED_HOSTS"]
        return raw_string.replace(" ", "").split(",")

    @property
    def jwt_allowed_issuer_hosts(self) -> list[str]:
        raw_string = self.__env["JWT_ALLOWED_ISSUER_HOSTS"]
        return raw_string.replace(" ", "").split(",")

    @property
    def mongo_connection(self) -> dict:
        raw_uri = self.__env["MONGO_URI"]
        raw_user = self.__env["MONGO_USER"]
        raw_password = self.__env["MONGO_PASSWORD"]
        raw_port = int(self.__env["MONGO_PORT"])
        raw_cert_path = self.__env["MONGO_CERTIFICATE_PATH"]
        connection = {"cert_path": None, "port": 27017, "uri": None, "user": None, "password": None}
        if raw_uri != "" and raw_port != 0:
            if raw_user == "":
                connection["port"] = raw_port
                connection["uri"] = raw_uri
                cert_path = self.project_root_folder / raw_cert_path
                if Path.exists(cert_path):
                    connection["cert_path"] = str(cert_path.absolute())
                else:
                    raise FileNotFoundError("Не найден файл сертификата (MONGO_CERTIFICATE_PATH)")
                return connection
            elif raw_cert_path == "":
                connection["port"] = raw_port
                connection["user"] = raw_user
                connection["password"] = raw_password
                connection["uri"] = raw_uri
                return connection
            else:
                raise FileNotFoundError("Данные для подключения mongodb не заполнены")
        else:
            raise FileNotFoundError("Данные для подключения mongodb заполнены не правильно")
