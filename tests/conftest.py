import json
from constants import TOP_STORIES_KEY, BODY, SENTENCES, URL, TITLE, TEXT
import pytest


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