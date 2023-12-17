import traceback
import os.path
import tempfile
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
import model.models as models
from model.database import get_db_engine
from config import *
from utils.user_utils import FakeToken
from utils import audio_utils as au
import utils.general_utils as gu
import logging


logger = logging.getLogger(__name__)

router = APIRouter()

db_engine = get_db_engine()


@router.post("/upload")
async def upload(token: str = None, file: UploadFile = File(...), db: Session = Depends(db_engine.get_db)):
    try:
        c_token = FakeToken()
        user = await c_token.reveal_token(token)
        if not user:
            raise HTTPException(status_code=400, detail="token not valid")
        contents = file.file.read()
        with tempfile.TemporaryDirectory(dir=config_temp_path) as temp:
            temp_path = os.path.join(temp, file.filename)
            logger.info(f"tmp_file = {temp_path}")
            with open(temp_path, 'wb') as f:
                f.write(contents)
            md5 = gu.generate_md5(temp_path)
            file_record = db.query(models.Audio).filter(models.Audio.file_md5 == md5).first()
            logger.info(f"record with same md5 {file_record}")
            audio_record = models.Audio()

            # file already exists
            if file_record and gu.check_file_md5(file_record.file_path, file_record.file_md5):
                # write new record
                audio_record.file_name = file_record.file_name
                audio_record.file_path = file_record.file_path
                audio_record.file_md5 = file_record.file_md5
                audio_record.file_type = file_record.file_type
                audio_record.user_id = user.id
            else:
                # store new file
                store_path = gu.generate_store_path(file.filename)
                with open(store_path, 'wb') as f:
                    f.write(contents)
                logger.info(f"write file success to {store_path}")
                logger.info(f"audio md5 {md5}")
                # write new record
                audio_record.file_name = file.filename
                audio_record.file_path = store_path
                audio_record.file_md5 = md5
                audio_record.file_type = file.filename.split('.')[-1].lower()
                audio_record.user_id = user.id
            db.add(audio_record)
            db.commit()
            logger.info(f"write info to db success")

    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(f"error message{e}")
        return {"message": f"Error occured wile uploading {e}"}
    finally:
        file.file.close()
    return {"message": f"Upload file {file.filename} success",
            "request_id": audio_record.id,
            "md5": audio_record.file_md5
            }


@router.get("/list")
async def list_audio(token: str = None, db: Session = Depends(db_engine.get_db)):
    # check user auth
    c_token = FakeToken()
    user = await c_token.reveal_token(token)
    if not user:
        raise HTTPException(status_code=400, detail="token not valid")
    audio_records = db.query(models.Audio).filter(models.Audio.user_id == user.id).all()
    print(audio_records)
    retuen_records = []
    for audio_item in audio_records:
        audio_dict = audio_item.__dict__
        logger.info(audio_dict)
        retuen_records.append({
            "request_id": audio_dict.get("id", None),
            "file_name": audio_dict.get("file_name", None),
            "create_time": audio_dict.get("create_time", None),
        })
    return {"message": retuen_records}


@router.get("/download")
async def download(token: str = None, request_id: int = None, db: Session = Depends(db_engine.get_db)):
    # check user auth
    c_token = FakeToken()
    user = await c_token.reveal_token(token)
    if not user:
        raise HTTPException(status_code=400, detail="token not valid")
    # check record
    audio_record = db.query(models.Audio).filter(models.Audio.id == request_id).first()
    if not audio_record:
        return {"message": f"can't find file by given id{request_id}"}
    # check user privilege
    if audio_record.user_id != user.id:
        return {"message": f"current user can't access this file"}
    # check file exist
    if not os.path.exists(audio_record.file_path):
        return {"message": f"file damaged"}

    return FileResponse(path=audio_record.file_path,
                        filename=audio_record.file_name,
                        media_type=f'audio/{audio_record.file_type}')


@router.get("/volume")
async def volume(token: str = None, request_id: int = None, audio_volume: int = 0,
                 db: Session = Depends(db_engine.get_db)):
    # check user auth
    c_token = FakeToken()
    user = await c_token.reveal_token(token)
    if not user:
        raise HTTPException(status_code=400, detail="token not valid")
    # check record
    audio_record = db.query(models.Audio).filter(models.Audio.id == request_id).first()
    if not audio_record:
        return {"message": f"can't find file by given id{request_id}"}
    # check user privilege
    if audio_record.user_id != user.id:
        return {"message": f"current user can't access this file"}
    # check file exist
    if not os.path.exists(audio_record.file_path):
        return {"message": f"file damaged"}

    audio_name = audio_record.file_name
    audio_type = audio_record.file_type
    audio_engine = au.get_audio_engine(audio_record.file_path)
    adjust_path = audio_engine.adjust_volume(audio_volume)
    adjust_name = audio_name[:len(audio_name)-len(audio_type)] + str(audio_volume) + "." + audio_type
    logger.info(adjust_name)
    logger.info(f"message: path is {adjust_path}")
    return FileResponse(path=adjust_path,
                        filename=adjust_name,
                        media_type=f'audio/{audio_type}',
                        background=BackgroundTask(au.clean_temp, adjust_path))

