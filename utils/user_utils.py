# from typing import *
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from datetime import datetime, timedelta
# from jose import JWTError, jwt
# from pydantic import BaseModel
import model.models as models
from model.database import get_db_engine
from passlib.context import CryptContext
import logging

logger = logging.getLogger(__name__)

db_engine = get_db_engine()

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# SECRET_KEY = "2760e0273b7fcd5c21990e91871d0c4474e38cfb4d9322bec8296fa145e5dee0"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 12


# ---- database operation

async def get_user(user_name: str) -> models.User or None:
    """
    get user instance by username
    :param user_name:
    :return: User
    """
    with next(db_engine.get_db()) as db:
        user_record = db.query(models.User).filter(models.User.user_name == user_name).first()
        logger.info(user_record)
        if user_record:
            return user_record
        else:
            return None


async def get_pass_by_username(user_name: str) -> str or None:
    """
    get encrypted password by username
    :param user_name:
    :return:
    """
    with next(db_engine.get_db()) as db:
        user_record = db.query(models.User).filter(models.User.user_name == user_name).first()
        if user_record:
            return user_record.password
        else:
            return None


async def auth_user(user_name: str, password: str) -> bool:
    """
    auth username and password
    :param user_name:
    :param password:
    :return:
    """
    hasher = Hasher()
    hashed_pwd = await get_pass_by_username(user_name)
    if hashed_pwd:
        return hasher.verify_password(plain_pwd=password, hashed_pwd=hashed_pwd)
    else:
        return False


# ---- auth operation

class Hasher:
    """
    encrypte password to store in database
    todo: frontend should encrypt the password before deliver to backend
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_pwd: str, hashed_pwd: str) -> bool:
        """ verify given password"""
        return self.pwd_context.verify(plain_pwd, hashed_pwd)

    def get_password_hash(self, password: str) -> str:
        """
        encrypt the password
        :param password:
        :return: hashed password
        """
        return self.pwd_context.hash(password)


class FakeToken:
    """
    pretend the token encrypt and decrypt
    """

    def __init__(self):
        self.hash = '_token123'

    @staticmethod
    def check_valid(token: str) -> bool:
        """
        check if session token expired
        :param token: token of the session
        :return: true or false
        """
        return True

    def generate_token(self, user_name: str, expire_time: str = None) -> str:
        """
        generate a token
        :param user_name:
        :param expire_time: token expired time
        :return: a token
        """
        return user_name + self.hash

    async def reveal_token(self, token: str) -> models.User or None:
        """
        get the user Instance by token
        :param token:
        :return:
        """
        if not self.check_valid(token):
            return None
        token_length = len(token)
        hash_length = len(self.hash)
        user_name = token[:token_length-hash_length]
        user = await get_user(user_name)
        return user

    @staticmethod
    def invalid_token(token: str) -> bool:
        """
        expire a token
        :param token:
        :return:
        """
        return True
