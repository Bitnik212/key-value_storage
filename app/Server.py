from enum import Enum

from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.core.middlewares import AppMiddleware
from app.core.App import App
from app.core.AppConfig import AppConfig
from app.middlewares.JWTMiddleware import JWTMiddleware
from app.routes import ServerRoutes


class Server(App):

    def __init__(self):
        super().__init__()
        self.routes: id(Enum) = ServerRoutes
        self.config = self._configure()
        self.debug: bool = False
        self.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    @staticmethod
    def _configure() -> AppConfig:
        app = AppConfig()
        app.title = "KeyWord Storage"
        app.version = "0.0.1"
        app.mount_path = "/"
        app.servers = [
            {"url": "http://0.0.0.0:8000/", "description": "Development server"},
        ]
        return app

