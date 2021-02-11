#RestAPIの入力設計に関するファイル
from pydantic import BaseModel
from typing import List


class Activity(BaseModel):
    url:str = "Enter the Target URL"
    tags:List[str] = [""]

class User(BaseModel):
    username: str = "Enter Your Name"
    password: str = "Enter The Password"
    premium:bool = False
