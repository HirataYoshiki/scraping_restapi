#RestAPIの入力設計に関するファイル
from pydantic import BaseModel
from typing import List,Optional


class Activity(BaseModel):
    url:str = "Enter the Target URL"
    tags:List[str] = [""]

class User(BaseModel):
    username: str = "Enter Your Name"
    password: str = "Enter The Password"
    premium:Optional[bool] = None

class UserOut(User):
    userid:int
    username:Optional[str]
    password:Optional[str]
    premium:Optional[bool]= None


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:Optional[str]=None