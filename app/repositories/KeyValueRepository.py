from fastapi import HTTPException
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from app.databases.MongoDB import MongoDB


class KeyValueRepository:
    OBJECT_ID_NAME = "_id"
    SERVER_ERROR = "Server error"

    def __init__(self):
        self.db: Database = MongoDB().connect()

    def __convert_value(self, storage_id: int, value: dict) -> dict:
        value.update({self.OBJECT_ID_NAME: storage_id})
        return value

    def __convert_key(self, storage_id: int) -> dict:
        return {self.OBJECT_ID_NAME: storage_id}

    async def set(self, storage_id: int, key: str, value: dict):
        try:
            await self.db.get_collection(key).insert_one(self.__convert_value(storage_id, value))
        except DuplicateKeyError as e:
            await self.update(storage_id, key, value)
        except Exception as e:
            print(e)
            raise HTTPException(detail=self.SERVER_ERROR, status_code=500)

    async def get(self, storage_id: int, key: str) -> dict or None:
        try:
            return await self.db.get_collection(key).find_one(self.__convert_key(storage_id))
        except Exception as e:
            print(e)
            raise HTTPException(detail=str(e), status_code=400)

    async def delete(self, storage_id: int, key: str) -> dict or None:
        item = await self.get(storage_id, key)
        if item is not None:
            try:
                await self.db.get_collection(key).delete_one(self.__convert_key(storage_id))
                return item
            except Exception as e:
                print(e)
                raise HTTPException(detail=self.SERVER_ERROR, status_code=500)
        else:
            return None

    async def update(self, storage_id: int, key: str, value: dict):
        try:
            await self.db.get_collection(key).update_one(self.__convert_key(storage_id), {"$set": value})
        except Exception as e:
            print(e)
            raise HTTPException(detail=self.SERVER_ERROR, status_code=500)


