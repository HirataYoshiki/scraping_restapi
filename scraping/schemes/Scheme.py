#データベース設計に関するファイル
from pydantic import BaseModel
from typing import List

class Activity(BaseModel):
    items:List[str]

class User(BaseModel):
    username: str
    password: str
    premium:bool = False