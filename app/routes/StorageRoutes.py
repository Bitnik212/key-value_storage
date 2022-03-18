from fastapi import APIRouter, Form, Depends

from app.core.models.HTTPErrors import HTTPErrors
from app.core.utils.ResponseBuilder import ResponseBuilder
from app.middlewares.JWTMiddleware import JWTMiddleware


class StorageRoutes:

    def __init__(self):
        """
        Хранилище пользователя
        """

    router = APIRouter()
    TAGS = ["Хранилище"]
    DEPENDENCIES = [Depends(JWTMiddleware())]

    @staticmethod
    @router.post(
        path="/add",
        responses=HTTPErrors().errors,
        tags=TAGS,
        summary="Добавить данные",
        dependencies=DEPENDENCIES
    )
    async def sign_in(key: str = Form(..., description="Ключ"), value: str = Form(..., description="Значение")):
        return ResponseBuilder().not_impl()
