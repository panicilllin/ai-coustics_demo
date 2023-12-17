import abc

from enum import Enum
from typing import *
from uuid import UUID, uuid4
from pydub import AudioSegment
from utils.general_utils import *
import logging

logger = logging.getLogger(__name__)


class AudioType(str, Enum):
    mp3 = "mp3"
    flac = "flac"
    wav = "wav"


class AudioEngine(metaclass=abc.ABCMeta):
    audio_id: Optional[UUID] = uuid4()
    file_name: str
    file_path: str
    file_md5: str  # check md5 to reduce duplicate files
    file_type: AudioType
    _audio_type = None
    SUBCLASSES = {}

    def __init__(self, file_path) -> None:
        logger.info(f"start init audio")
        self.file_name = os.path.basename(file_path)
        self.file_path = file_path
        self.file_md5 = generate_md5(self.file_path)  # check md5 to reduce duplicate files
        self.file_type = AudioType(self.file_name.split('.')[-1].lower())
        # user: User  # user who upload this file

    def __init_subclass__(cls, **kwargs):
        """
        child hook
        """
        super().__init_subclass__(**kwargs)
        cls.SUBCLASSES[cls._audio_type] = cls

    @classmethod
    def create(cls, audio_type, params):
        if audio_type not in cls.subclasses:
            raise ValueError(f'Bad audio type {audio_type}')

        return cls.subclasses[audio_type](params)

    def adjust_volume(self, volume: int):
        pass

    @property
    def dbfs(self) -> AudioSegment.dBFS:
        audio = AudioSegment.from_file(self.file_path)
        return audio.dBFS


class MP3Engine(AudioEngine):
    _audio_type = AudioType('mp3')

    def __init__(self, file_path):
        logger.info(f"initing MP3Engine")
        super().__init__(file_path)

    def adjust_volume(self, volume: int = 0):
        audio = AudioSegment.from_mp3(self.file_path)
        if volume > 10 or volume < -10:
            return None
        if volume == 0:
            return self.file_path
        else:
            adjust_song = audio + volume
            store_path = generate_temp_path(self.file_name)
            adjust_song.export(store_path, format='mp3')
            return store_path


class FLACEngine(AudioEngine):
    _audio_type = AudioType('flac')

    def __init__(self, file_name):
        logger.info(f"initing FLACEngine")
        super().__init__(file_name)

    def adjust_volume(self, volume: int = 0):
        audio = AudioSegment.from_file(self.file_path)
        if volume > 10 or volume < -10:
            return None
        if volume == 0:
            return self.file_path
        else:
            adjust_song = audio + volume
            store_path = generate_temp_path(self.file_name)
            logger.info(f"store_path = {store_path}")
            adjust_song.export(store_path, format='flac')
            return store_path


class WAVEngine(AudioEngine):
    _audio_type = AudioType('wav')

    def __init__(self, file_name):
        super().__init__(file_name)


# ---------

def get_audio_engine(file_path: str) -> AudioEngine:
    _cls = AudioEngine(file_path)
    _scls = _cls.SUBCLASSES.get(AudioType(_cls.file_type), None)
    if not _scls:
        raise
    instance = _scls(file_path)
    return instance


if __name__ == "__main__":
    pass
