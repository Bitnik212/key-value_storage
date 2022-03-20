from fastapi import APIRouter, Depends, Body, Security
from fastapi.params import Query
from fastapi.security import HTTPAuthorizationCredentials
from app.core.models.HTTPErrors import HTTPErrors
from app.core.utils.ResponseBuilder import ResponseBuilder
from app.middlewares.JWTMiddleware import JWTMiddleware
from app.repositories.KeyValueRepository import KeyValueRepository

repository = KeyValueRepository()
security = JWTMiddleware()

"""
Хранилище зарегистрированных пользователей
"""

router = APIRouter(
    prefix="/items"
)
TAGS = ["Хранилище"]
DEPENDENCIES = [Depends(JWTMiddleware())]


@router.post(
    path="/",
    responses=HTTPErrors().errors,
    tags=TAGS,
    summary="Добавить/обновить данные",
    dependencies=DEPENDENCIES
)
async def set(
    credentials: HTTPAuthorizationCredentials = Security(security),
    key: str = Query(..., description="Ключ"),
    value: dict = Body(..., description="Значение")
):
    user_id = security.util.get_user_id(credentials.credentials)
    await repository.set(storage_id=user_id, key=key, value=value)
    return ResponseBuilder.success()


@router.get(
    path="/",
    responses=HTTPErrors().errors,
    tags=TAGS,
    summary="Получить данные",
    dependencies=DEPENDENCIES
)
async def get(credentials: HTTPAuthorizationCredentials = Security(security), key: str = Query(..., description="Ключ")):
    user_id = security.util.get_user_id(credentials.credentials)
    result = await repository.get(storage_id=user_id, key=key)
    if result is None:
        return ResponseBuilder.not_found()
    return ResponseBuilder.result(data=result)


@router.delete(
    path="/",
    responses=HTTPErrors().errors,
    tags=TAGS,
    summary="Удалить данные",
    dependencies=DEPENDENCIES
)
async def delete(credentials: HTTPAuthorizationCredentials = Security(security), key: str = Query(..., description="Ключ")):
    user_id = security.util.get_user_id(credentials.credentials)
    result = await repository.delete(storage_id=user_id, key=key)
    if result is None:
        return ResponseBuilder.not_found()
    return ResponseBuilder.result(data=result)
