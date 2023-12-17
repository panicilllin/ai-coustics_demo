import os
import traceback
import uuid
import hashlib
from tempfile import mkdtemp

from config import config_audio_path, config_temp_path
import logging
logger = logging.getLogger(__name__)


def generate_md5(file_path: str) -> [str, None]:
    logger.debug(f"generate_md5:: file_path is {file_path}")
    if not os.path.exists(file_path):
        logger.info(f"generate_md5:: file_path {file_path} not exist")
        return None

    with open(file_path, "rb") as f:
        file_hash = hashlib.md5()
        while chunk := f.read(8192):
            file_hash.update(chunk)
    return file_hash.hexdigest()


def check_file_md5(file_path: str, md5: str) -> bool:
    logger.debug(f"check_file_md5:: file_path={file_path};md5={md5}")
    if md5 == generate_md5(file_path):
        return True
    return False


# not useful now switch to tempfile lib
# def genetate_temp_path_abandon(file_name: str) -> [str, None]:
#     temp_file_path = None
#     try:
#         temp_file_name = str(uuid.uuid4()) + '.' + file_name.split('.')[-1]
#         temp_file_path = os.path.join(config_temp_path, temp_file_name)
#         return temp_file_path
#     finally:
#         clean_temp(temp_file_path)


def generate_store_path(file_name: str) -> str:
    os.makedirs(config_audio_path, exist_ok=True)
    store_name = str(uuid.uuid4()) + '.' + file_name.split('.')[-1]
    store_path = os.path.join(config_audio_path, store_name)
    return store_path


def generate_temp_path(file_name: str) -> str:
    os.makedirs(config_audio_path, exist_ok=True)
    temp_path = mkdtemp(dir=config_temp_path)
    temp_path = os.path.join(temp_path, file_name)
    return temp_path


def clean_temp(tmp_file_path:str) -> bool:
    """
    remove temp file and dir
    :param tmp_file_path: file path gonna remove
    :return:
    """
    # remove tmp file
    if os.path.exists(tmp_file_path):
        logger.info(f"gonna remove file {tmp_file_path}")
        os.remove(tmp_file_path)
    try:
        # remove tmp folder
        base_path = config_temp_path
        tmp_file_dir = os.path.dirname(os.path.relpath(tmp_file_path, base_path))
        if tmp_file_dir:
            abs_path = os.path.join(base_path, tmp_file_dir)
            logger.info(f"gonna remove dir {abs_path}")
            os.rmdir(abs_path)
    except Exception as e:
        logger.info(traceback.format_exc())
        logger.info(e)
    # finally:
    return True
