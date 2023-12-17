import pytest
import utils.general_utils as gu


def test_generate_md5():
    audio_path = "./test_audio.flac"
    md5 = gu.generate_md5(audio_path)
    assert md5 == "cb7fcf2557d00eb3a93a731a2f03848e"


def test_check_file_md5():
    audio_path = "./test_audio.flac"
    res_true = gu.check_file_md5(audio_path, "cb7fcf2557d00eb3a93a731a2f03848e")
    assert res_true is True
    res_false = gu.check_file_md5(audio_path, "1111111111111111111111111111111")
    assert res_false is False
