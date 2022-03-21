from random import Random

from fastapi import HTTPException
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from app.databases.MongoDB import MongoDB


class KeyValueRepository:
    OBJECT_ID_NAME = "_id"
    SERVER_ERROR = "Server error"
    ANON_COLLECTION_NAME = "anon_id_registry"
    ANON_ID_PREFIX = "anon_"
    MIN_ANON_RANDOM_STORAGE_ID = 10
    MAX_ANON_RANDOM_STORAGE_ID = 900000

    def __init__(self):
        self.db: Database = MongoDB().connect()

    def __convert_value(self, storage_id: int, value: dict, is_anon: bool = False) -> dict:
        value.update(self.__convert_key(storage_id, is_anon))
        return value

    def __convert_key(self, storage_id: int, is_anon: bool = False) -> dict:
        if is_anon:
            return {self.OBJECT_ID_NAME: self.ANON_ID_PREFIX+str(storage_id)}
        else:
            return {self.OBJECT_ID_NAME: storage_id}

    async def set(self, storage_id: int, key: str, value: dict, is_anon: bool = False):
        try:
            await self.db.get_collection(key).insert_one(self.__convert_value(storage_id, value, is_anon))
            if is_anon:
                await self.handle_anon_storage_id(storage_id)
        except DuplicateKeyError as e:
            await self.update(storage_id, key, value, is_anon)
        except Exception as e:
            print(e)
            raise HTTPException(detail=self.SERVER_ERROR, status_code=500)

    async def get(self, storage_id: int, key: str, is_anon: bool = False) -> dict or None:
        try:
            return await self.db.get_collection(key).find_one(self.__convert_key(storage_id, is_anon))
        except Exception as e:
            print(e)
            raise HTTPException(detail=str(e), status_code=400)

    async def delete(self, storage_id: int, key: str, is_anon: bool = False) -> dict or None:
        item = await self.get(storage_id, key, is_anon)
        if item is not None:
            try:
                await self.db.get_collection(key).delete_one(self.__convert_key(storage_id, is_anon))
                return item
            except Exception as e:
                print(e)
                raise HTTPException(detail=self.SERVER_ERROR, status_code=500)
        else:
            return None

    async def update(self, storage_id: int, key: str, value: dict, is_anon: bool = False):
        try:
            await self.db.get_collection(key).update_one(self.__convert_key(storage_id, is_anon), {"$set": value})
        except Exception as e:
            print(e)
            raise HTTPException(detail=self.SERVER_ERROR, status_code=500)

    async def get_random_anon_storage_id(self) -> int:
        random_id = Random().randint(self.MIN_ANON_RANDOM_STORAGE_ID, self.MAX_ANON_RANDOM_STORAGE_ID)
        finded = await self.db.get_collection(self.ANON_COLLECTION_NAME).find_one(self.__convert_key(random_id, True))
        if finded is None:
            return random_id
        else:
            await self.get_random_anon_storage_id()

    async def handle_anon_storage_id(self, storage_id: int):
        try:
            await self.db.get_collection(self.ANON_COLLECTION_NAME).insert_one(self.__convert_key(storage_id, True))
        except DuplicateKeyError as e:
            pass
