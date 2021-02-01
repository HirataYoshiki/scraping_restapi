from fastapi import APIRouter

from schemes import Scheme
from models import Model
from controls import Control

import hashlib
import datetime

router = APIRouter()

@router.get('/')
async def api_schemas():
    result = {
        '/':{'get':'api_schemas',
            '/users':{
                'get':"get all data about users",
                'post':"",
                'put':"",
                '/{userid}':{
                    "get":"",
                    "put":"",
                    'delete':""
                }
            },
            '/activities':{
                'get':"",
                '/{activityid}':{
                    'get':"",
                    'delete':""
                }
            }
        }
    }
    return result

class RouterUsers:
    @router.get('/users')
    async def get_all_users():
        query = Model.SessionLocal.query(Model.User).all()
        return query

    @router.post('/users')
    async def add_new_user(
        user:Scheme.User):
        name = user.username
        password = hashlib.sha256(user.password.encode()).hexdigest()
        adds = Model.User(
            name = name,
            password = password
            )
        Model.SessionLocal.add(adds)
        Model.SessionLocal.commit()

        return {
            "items":Model.SessionLocal.query(Model.User).filter(Model.User.name == name).all(),
            "condition":True
            }

    @router.get('/users/{userid}')
    async def get_user(
        userid:int):
        result = Model.SessionLocal.query(Model.User).filter(Model.User.userid == userid).one()
        return {"items":result}

    @router.put('/users/{userid}')
    async def update_user(
        userid:int,
        user:Scheme.User):
        updates = Model.SessionLocal.query(Model.User).filter(Model.User.userid==userid).first()
        if user.username:
            updates.name = user.username
        if user.premium:
            updates.premium = True

        Model.SessionLocal.commit()

    @router.delete('/users/{userid}')
    def delete_user(userid:int):
        delete = Model.SessionLocal.query(Model.User).filter(Model.User.userid== userid).first().delete()
        Model.SessionLocal.commit()
        return {
            "result":{
                "delete id":userid
                }
            }

class RoutersActivity:
    @router.post('/activities')
    def post_activity(activities:Scheme.Activity):
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
        Model.SessionLocal.add(adds)
        Model.SessionLocal.commit()

        return {
            "url":url,
            "tags":tags,
            "result":items
            }

    @router.get('/activities')
    def get_all_activities():
        query = Model.SessionLocal.query(Model.Activity).all()
        return {
            "result":query
        }

