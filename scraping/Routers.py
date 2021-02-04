#ルーターに対するレスポンスに関するファイル
from fastapi import APIRouter

from schemes import Scheme
from models import Model
from controls import Control

import hashlib
import datetime

router = APIRouter()

@router.get('/')
def api_schemas():
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
    return result

class RouterUsers:
    @router.get('/users')
    async def get_all_users():
        session = Model.get_session()
        query = session.query(Model.User).all()
        return query

    @router.post('/users')
    async def add_new_user(user:Scheme.User):
        session = Model.get_session()
        name = user.username
        password = hashlib.sha256(user.password.encode()).hexdigest()
        adds = Model.User(
            name = name,
            password = password
            )
        session.add(adds)
        try:
            session.commit()
        except:
            session.rollback()
            print("ロールバック")

        return {
            "items":session.query(Model.User).filter(Model.User.name == name).all(),
            "condition":True
            }

    @router.get('/users/{userid}')
    async def get_user(
        userid:int):
        session = Model.get_session()
        result = session.query(Model.User).filter(Model.User.userid == userid).one()
        return {
            "items":result
            }

    @router.put('/users/{userid}')
    async def update_user(
        userid:int,
        user:Scheme.User):
        session = Model.get_session()
        updates = session.query(Model.User).filter(Model.User.userid==userid).one()
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
            "url":url,
            "tags":tags,
            "result":items
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
            "result":{
                "delete id":activityid
                }
            }



