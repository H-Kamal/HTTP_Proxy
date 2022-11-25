from typing import List

from pydantic import BaseModel

class URL_look_up(BaseModel):
    url: str
    allowed: bool

    class Config:
        orm_mode = True

class URL_look_up_create(URL_look_up):
    pass