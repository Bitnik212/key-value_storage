from enum import Enum

from app.routes import AnonStorageRoutes
from app.routes import StorageRoutes


class ServerRoutes(Enum):
    storage = StorageRoutes.router
    anon_storage = AnonStorageRoutes.router
