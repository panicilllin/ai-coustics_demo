import main
import pytest
from fastapi.testclient import TestClient
from utils.general_utils import clean_temp, generate_md5
from utils.audio_utils import get_audio_engine

app = main.app
client = TestClient(app)


#  ## test Fastapi url

def test_user_create():
    """
    test /api/user/create
    :return:
    """
    response = client.post("/api/user/create",
                           params={"user_name": "tester", "password": "tester_pass"}
                           )
    print(response.json())
    assert response.status_code in [200, 400]
    assert response.json() in [{"message": "User tester created"}, {'detail': 'this user name already exist'}]


def test_user_login():
    response = client.post("/api/user/login",
                           params={"user_name": "tester", "password": "tester_pass"}
                           )
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {'access_token': 'tester_token123', 'token_type': 'fake'}


def test_audio_upload():
    file_path = "./test_audio.flac"
    response = client.post("/api/audio/upload",
                           params={"token": "tester_token123"},
                           files={"file": ("test_audio.flac", open(file_path, "rb"), "aduio/flac")}
                           )
    print(f"\n{response.json()}")
    assert response.status_code == 200
    assert response.json().get("message", None) == 'Upload file test_audio.flac success'


def test_audio_list():
    file_path = "./test_audio.flac"
    response = client.get("/api/audio/list",
                          params={"token": "tester_token123"}
                          )
    print(f"\n{response.json()}")
    assert response.status_code == 200


def test_audio_get():
    audio_path = "./test_audio.flac"
    download_path = "./test_audio_download.flac"
    clean_temp(download_path)
    response = client.get("/api/audio/download",
                          params={"token": "tester_token123", "request_id": '1'}
                          )
    print(f"\n{response}")
    assert response.status_code == 200
    with open(download_path, 'wb') as f:
        f.write(response.content)
    assert generate_md5(download_path) == generate_md5(audio_path)
    clean_temp(download_path)


def test_audio_volume():
    audio_path = "./test_audio.flac"
    adjust_path = "./test_audio_adjust.flac"
    clean_temp(adjust_path)
    response = client.get("/api/audio/volume",
                          params={"token": "tester_token123", "request_id": "1", "audio_volume": "-5"}
                          )
    print(f"\n{response}")
    assert response.status_code == 200
    with open(adjust_path, 'wb') as f:
        f.write(response.content)

    org_audio = get_audio_engine(audio_path)
    adjust_audio = get_audio_engine(adjust_path)
    org_dbfs = org_audio.dbfs
    adjust_dbfs = adjust_audio.dbfs
    assert round(adjust_dbfs, 2) == round(org_dbfs - 5, 2)
    clean_temp(adjust_path)


def test_not_support_type():
    """
    test if upload a file that not support yet
    :return:
    """
    file_path = "./test_audio.txt"
    response = client.post("/api/audio/upload",
                           params={"token": "tester_token123"},
                           files={"file": ("test_audio.txt", open(file_path, "rb"), "aduio/flac")}
                           )
    print(f"\n{response.json()}")
    print(response.status_code)
    assert response.status_code == 415
    assert response.json() == {'detail': 'file Type not Support'}
