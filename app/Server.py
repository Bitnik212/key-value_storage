from enum import Enum

from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.ServerConfig import ServerConfig
from app.core.App import App
from app.core.AppConfig import AppConfig
from app.routes import ServerRoutes


class Server(App):

    def __init__(self):
        super().__init__()
        self.routers: id(Enum) = ServerRoutes
        self.server_config = ServerConfig()
        self.config = self._configure()
        self.debug: bool = False
        self.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    def _configure(self) -> AppConfig:
        app = AppConfig()
        app.title = self.server_config.application_title
        app.version = self.server_config.application_version
        app.mount_path = self.server_config.application_mount_path
        app.servers = []
        return app

