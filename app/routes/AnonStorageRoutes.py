from fastapi import APIRouter
from fastapi.params import Body, Query

from app.core.models.HTTPErrors import HTTPErrors
from app.core.utils.ResponseBuilder import ResponseBuilder
from app.repositories.KeyValueRepository import KeyValueRepository

repository = KeyValueRepository()

"""
Хранилище анонимных пользователей
"""

router = APIRouter(prefix="/anon/items")
TAGS = ["Анонимное хранилище"]


@router.post(
    path="/",
    responses=HTTPErrors().errors,
    tags=TAGS,
    summary="Добавить/обновить данные",
)
async def set(
    storage_id: int = Query(..., description="Просто id по которому можно получить данные"),
    key: str = Query(..., description="Ключ"),
    value: dict = Body(..., description="Значение")
    ):
    await repository.set(storage_id=storage_id, key=key, value=value)
    return ResponseBuilder.success()


@router.get(
    path="/",
    responses=HTTPErrors().errors,
    tags=TAGS,
    summary="Получить данные",
)
async def get(
        storage_id: int = Query(..., description="Просто id по которому можно получить данные"),
        key: str = Query(..., description="Ключ")
):
    result = await repository.get(storage_id=storage_id, key=key)
    if result is None:
        return ResponseBuilder.not_found()
    return ResponseBuilder.result(data=result)


@router.delete(
    path="/",
    responses=HTTPErrors().errors,
    tags=TAGS,
    summary="Удалить данные",
)
async def delete(
        storage_id: int = Query(..., description="Просто id по которому можно получить данные"),
        key: str = Query(..., description="Ключ")
):
    result = await repository.delete(storage_id=storage_id, key=key)
    if result is None:
        return ResponseBuilder.not_found()
    return ResponseBuilder.result(data=result)
