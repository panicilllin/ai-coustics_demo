from datetime import datetime
from typing import *
from pydantic import BaseModel
from uuid import UUID, uuid4
from typing import *
from enum import Enum

# this file not in use for now


class AudioType(str, Enum):
    mp3 = "mp3"
    flac = "flac"
    wav = "wav"


class User(BaseModel):
    user_id: Optional[UUID] = uuid4()
    user_name: str
    password: str


class Audio(BaseModel):
    audio_id: Optional[UUID] = uuid4()
    file_name: str
    file_path: str
    file_md5: str  # check md5 to reduce duplicate files
    file_type: AudioType
    user_id: User.user_id  # user who upload this file
    create_time: datetime
