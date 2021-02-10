#RestAPIの入力設計に関するファイル
from pydantic import BaseModel
from typing import List
from dataclasses import dataclass,asdict


class Activity(BaseModel):
    url:str = "Enter the Target URL"
    tags:List[str] = [""]

@dataclass
class User(BaseModel):
    username: str = "Enter Your Name"
    password: str = "Enter The Password"
    premium:bool = False
