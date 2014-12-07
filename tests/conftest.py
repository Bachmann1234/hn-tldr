import json
from constants import AYLIEN_ID, REDIS_PORT, REDIS_PASS, REDIS_HOST, TOP_STORIES_KEY, BODY, TEXT, SENTENCES, TITLE, URL
from constants import AYLIEN_KEY
from main import app
import pytest


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch):
    monkeypatch.setenv(AYLIEN_ID, 'fakeid')
    monkeypatch.setenv(AYLIEN_KEY, 'fakekey')
    monkeypatch.setenv(REDIS_HOST, 'fakehost')
    monkeypatch.setenv(REDIS_PORT, '23123')
    monkeypatch.setenv(REDIS_PASS, 'fakepass')


@pytest.fixture()
def fake_redis_store():
    return {
        TOP_STORIES_KEY: json.dumps([8712349, 8712417, 8712277]).encode('utf-8'),
        b'8712349': json.dumps(
            {BODY: {
                TEXT: 'one\ntwo\nthree',
                SENTENCES: ['one', 'two', 'three']
            },
                URL: 'http://totalurl.com',
                TITLE: 'I am a title!'
            }
        ).encode('utf-8'),
        b'8712417': json.dumps(
            {BODY: {
                TEXT: 'four\nfive\nsix',
                SENTENCES: ['four', 'five', 'six']
            },
                URL: 'http://real.com',
                TITLE: 'I am a second title!'
            }
        ).encode('utf-8'),
        b'8712277': json.dumps(
            {BODY: {
                TEXT: 'seven',
                SENTENCES: []  # Sometimes api fails to summarize
            },
                URL: 'http://imathingy.com',
                TITLE: 'I am a third title!'
            }
        ).encode('utf-8')
    }


@pytest.fixture
def test_app():
    return app.test_client()
