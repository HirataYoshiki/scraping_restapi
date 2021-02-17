from datetime import datetime, timedelta
from typing import Optional
import hashlib

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from models.Model import get_session,User
from schemes.Scheme import Token,TokenData,UserOut
import config
"""
[Autholization]
      in this file, I'll make OAuth2.0 autholization.
      if other FrontEnd Engeneer want to use my API server, they have to send request to get access token.

      [request flow]
      1. Post (username,password) to /token
      2. Check if username and password is in DB
          .case1 if not user in DB, return HttpException400
          .case2 if not password in DB, return HttpException400
      3. Authentificate complete return token
      now everyone in DataBase:User can use API
      and next I'll check if the user is premium or not
      4. Check if premium status is active or not
          .case1 if not active, return HttpException401
          .case2 if active, continue 
"""


def verify_password(plain_password, hashed_password)->bool:
      if hashlib.sha256(plain_password.encode()).hexdigest()==hashed_password:
            return True
      else:
            return False
      #return config.PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password):
      return config.PWD_CONTEXT.hash(password)


def get_user(session, username: str):
      try:
            user_data = session.query(User).filter(User.username==username).one()
            return user_data
      except:
            return False


def authenticate_user(session, username: str, password: str):
      user_data = session.query(User).filter(User.username==username).one()
      if not user_data:
            return False
      if not verify_password(password, user_data.password):
            return False
      return user_data


def create_access_token(user_data:dict, expires_delta: Optional[timedelta] = None):
      to_encode = user_data.copy()
      if expires_delta:
            expire = datetime.utcnow() + expires_delta
      else:
            expire = datetime.utcnow() + timedelta(minutes=15)
      to_encode.update({"exp": expire})
      encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
      return encoded_jwt

async def get_current_user(token: str = Depends(config.OAUTH2_SCHEME)):
      credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
      )
      try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                  raise credentials_exception
            token_data = TokenData(username=username)
      except JWTError:
            raise credentials_exception
      user = get_user(get_session(), username=token_data.username)
      if not user:
            raise credentials_exception
      return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
      if not current_user.premium:
            raise HTTPException(status_code=400, detail="Inactive user")
      return current_user



