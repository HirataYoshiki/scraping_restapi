#ルーターに対するレスポンスに関するファイル
from fastapi import APIRouter,Request ,Response, Header,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from typing import List,Optional

from schemes import Scheme
from models import Model
from controls import Control
from autholization.Auth import Autholization
Auth = Autholization()

import hashlib
import datetime
import os
from datetime import datetime, timedelta

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__),"../frontend/templates"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



#entry point to HomePage
@router.get('/',response_class=HTMLResponse)
async def api_schemas(request:Request,responce:Response,token: str = Depends(oauth2_scheme)):
    result = {
            '/':{'get':'api_schemas',
                '/users':{
                    'get':"get all data about users",
                    'post':"register new user with username,password",
                    'put':"",
                    '/{userid}':{
                        "get":"get info about the user",
                        "put":"change info about the user",
                        'delete':"delete the user"
                    }
                },
                '/activities':{
                    'get':"get all info about activities",
                    '/{activityid}':{
                        'get':"get info about the activity",
                        'delete':""
                    }
                }
            }
        }
    return templates.TemplateResponse(
        "index.html",
        {
            "request":request,
            "data":"basics",
            "contents":token
            }
        )

@router.get('/login')
async def api_schemas(responce:Response,user_agent: Optional[str] = Header(None)):
    print(user_agent)
    return {"items":[{"name":"login"}]}


class RouterUsers:
    @router.get('/users')
    async def get_all_users():
        session = Model.get_session()
        query = session.query(Model.User).all()
        return {"items":query}

    @router.post('/users')
    async def add_new_user(user:Scheme.User):
        session = Model.get_session()
        name = user.username
        password = hashlib.sha256(user.password.encode()).hexdigest()
        adds = Model.User(
            name = name,
            password = password,
            premium = user.premium
            )
        session.add(adds)
        try:
            session.commit()
        except:
            session.rollback()
            print("ロールバック")

        return {
            "items":session.query(Model.User).filter(Model.User.name == name).one()
            }

    @router.get("/users/me/", response_model=Scheme.User)
    async def read_users_me(current_user: Scheme.User = Depends(Auth.get_current_active_user)):
        return current_user

    @router.put('/users/{userid}')
    async def update_user(
        userid:int,
        user:Scheme.User):
        session = Model.get_session()
        updates = session.query(Model.User).filter(Model.User.userid==userid).one()
        print(updates)
        if user.username:
            updates.name = user.username
        if user.premium:
            updates.premium = True

        try:
            session.commit()
        except:
            session.rollback()
            print("ロールバック")
        return {
            "item":updates}

    @router.delete('/users/{userid}')
    async def delete_user(userid:int):
        session = Model.get_session()
        delete = session.query(Model.User).filter(Model.User.userid== userid).one()
        session.delete(delete)
        try:
            session.commit()
        except:
            session.rollback()
            print("ロールバック")
        return {
            "result":{
                "delete id":userid
                }
            }

class RoutersActivity:
    @router.post('/activities')
    async def post_activity(activities:Scheme.Activity):
        session = Model.get_session()
        url = activities.url
        tags = activities.tags
        action = {
            "url":url,
            "tags":tags
            }
        
        items = Control.Scraping.get_results(url,tags)
        adds = Model.Activity(
            userid = 111,
            timestamp = datetime.datetime.now(),
            action = str(action),
            items = str(items)
        )
        session.add(adds)
        try:
            session.commit()
        except:
            session.rollback()
            print("ロールバック")
        return {
            "items":[{
                "url":url,
                "tags":tags,
                "result":items
                }]
            }

    @router.get('/activities')
    async def get_all_activities():
        session = Model.get_session()
        query = session.query(Model.Activity).all()
        return {
            "result":query
        }

    @router.delete('/activities/{activityid}')
    def delete_activity(activityid:int):
        session = Model.get_session()
        deletes = session.query(Model.Activity).filter(Model.Activity.id == activityid).one()
        session.delete(deletes)
        try:
            session.commit()
        except:
            session.rollback()
            print("ロールバック")
        return {
            "items":[{
                "delete id":activityid
                }]
            }

class OAuth_Token:
    @router.post("/token", response_model=Scheme.Token)
    async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        session = Model.get_session()
        user = Auth.authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=Auth.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = Auth.create_access_token(
            user_data={"sub": user.name}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


