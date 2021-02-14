from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext

#For Auth.py
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "ce8eea207e86e3f4544e23b6cde3faa557d959f78ab3ce3f48a7d30d84752638"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30