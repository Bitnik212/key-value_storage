from enum import Enum

from app.routes.StorageRoutes import StorageRoutes


class ServerRoutes(Enum):
    signIn = StorageRoutes.router

