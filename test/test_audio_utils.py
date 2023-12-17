import sys

import pytest

from utils.audio_utils import AudioEngine, AudioType, get_audio_engine


def test_subclass():
    audio_path = 'test./02. Rain.flac'
    from utils.audio_utils import AudioEngine, AudioType
    cls = AudioEngine(audio_path)
    scls = cls.SUBCLASSES.get(AudioType(cls.file_type))
    inst = scls(audio_path)
    print(f"\ncls.SUBCLASSES=={cls.SUBCLASSES}")
    assert scls.__name__ == "FLACEngine"
    print(f"inst = {inst.file_path}")


def test_get_audio_engine():
    audio_path = 'test./02. Rain.flac'
    engine = get_audio_engine(audio_path)
    assert engine.file_path == audio_path
    assert engine._audio_type == AudioType('flac')


