from typing import Union

from pydantic import BaseModel


class DefaultResponseModel(BaseModel):
    data: Union[dict, None]
    info: str or None
