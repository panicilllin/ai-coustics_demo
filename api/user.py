import model.models as models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from config import config_token_valid_time
from model.database import get_db_engine
from utils.user_utils import get_user, auth_user, Hasher, FakeToken
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

db_engine = get_db_engine()


@router.post("/create", status_code=status.HTTP_200_OK)
async def create_account(user_name: str, password: str, db: Session = Depends(db_engine.get_db)):
    """
    creat user accound
    :param user_name:
    :param password:
    :param db: database session
    :return: json
    """
    if await get_user(user_name):
        raise HTTPException(status_code=400, detail="this user name already exist")
    hasher = Hasher()
    user_record = models.User()
    user_record.user_name = user_name
    user_record.password = hasher.get_password_hash(password)
    db.add(user_record)
    db.commit()
    logger.info(f"write info to db success")
    return {"message": f"User {user_name} created"}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_name: str, password: str):
    """
    login with username and password
    :param user_name:
    :param password:
    :return: fake token for other api usage
    """
    if not user_name and password:
        raise HTTPException(status_code=400, detail="user name or password not given")
    user = await get_user(user_name)
    if not user:
        raise HTTPException(status_code=400, detail="user not exist")

    # hasher = Hasher()
    if not await auth_user(user_name, password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    c_token = FakeToken()
    access_token = c_token.generate_token(user_name=user_name, expire_time=config_token_valid_time)
    return {"access_token": access_token, "token_type": "fake"}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(token: str):
    """
    Not yet implemented
    :param token: user token
    :return: json
    """
    c_token = FakeToken()
    c_token.invalid_token(token)
    return {"message": f"try pretend you're log out"}
