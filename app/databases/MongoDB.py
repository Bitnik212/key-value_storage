from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from pymongo.server_api import ServerApi

from app.ServerConfig import ServerConfig


class MongoDB:

    def __init__(self):
        self.__env = ServerConfig()
        self.__connection_dict: dict = self.__env.mongo_connection
        self.__uri: str or None = self.__env.mongo_connection["uri"]
        self.__port: int = self.__env.mongo_connection["port"]
        self.__cert_path: str or None = self.__env.mongo_connection["cert_path"]
        self.__user: str or None = self.__env.mongo_connection["user"]
        self.__password: str or None = self.__env.mongo_connection["password"]
        self.database_name: str = "bitreader"

    def connect(self) -> Database:
        if self.__cert_path:
            client = AsyncIOMotorClient(
                self.__uri,
                tls=True,
                tlsCertificateKeyFile=self.__cert_path,
                server_api=ServerApi('1'),
                port=self.__port
            )
        else:
            client = AsyncIOMotorClient(
                host=self.__uri,
                username=self.__user,
                password=self.__password,
                server_api=ServerApi('1'),
                port=self.__port
            )
        return client.get_database(name=self.database_name)
