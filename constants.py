import os

TOP_STORIES_KEY = b'top_30'
TITLE = 'title'
URL = 'url'
BODY = 'body'
SENTENCES = 'sentences'
HACKER_NEWS_ID = 'hn_id'
TEXT = 'text'
DATE_FOUND = 'date_found'
AYLIEN_ID = 'AYLIENID'
AYLIEN_KEY = 'AYLIENKEY'
REDIS_HOST = 'REDIS_HOST'
REDIS_PORT = 'REDIS_PORT'
REDIS_PASS = 'REDIS_PASS'


def get_environment():
    return {
        AYLIEN_ID: os.environ.get(AYLIEN_ID),
        AYLIEN_KEY: os.environ.get(AYLIEN_KEY),
        REDIS_HOST: os.environ.get(REDIS_HOST),
        REDIS_PORT: int(os.environ.get(REDIS_PORT), 0),
        REDIS_PASS: os.environ.get(REDIS_PASS),
    }
