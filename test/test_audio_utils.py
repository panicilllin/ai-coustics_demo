import pytest

from utils.audio_utils import AudioType, get_audio_engine
from utils.general_utils import clean_temp


def test_subclass():
    audio_path = './test/02. Rain.flac'
    from utils.audio_utils import AudioEngine, AudioType
    cls = AudioEngine(audio_path)
    scls = cls.SUBCLASSES.get(AudioType(cls.file_type))
    inst = scls(audio_path)
    print(f"\ncls.SUBCLASSES=={cls.SUBCLASSES}")
    assert scls.__name__ == "FLACEngine"
    print(f"inst = {inst.file_path}")


def test_get_audio_engine():
    audio_path = './test/02. Rain.flac'
    audio_engine = get_audio_engine(audio_path)
    assert audio_engine.file_path == audio_path
    assert audio_engine._audio_type == AudioType('flac')


def test_volume_adjust():
    audio_path = 'test_audio.flac'
    org_audio = get_audio_engine(audio_path)
    org_dbfs = org_audio.dbfs
    adjusted_path = org_audio.adjust_volume(-3)
    adjust_audio = get_audio_engine(adjusted_path)
    adjust_dbfs = adjust_audio.dbfs
    assert round(adjust_dbfs, 2) == round(org_dbfs - 3, 2)
    clean_temp(adjusted_path)
