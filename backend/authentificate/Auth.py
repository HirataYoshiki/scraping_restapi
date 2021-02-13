from fastapi import Request ,Response, Header
from models.Model import get_session

#from cookie check if username & password exists
def check_name_password(func):
      def wrap(*args,**kwargs):
             