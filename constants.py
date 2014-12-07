import os

TOP_STORIES_KEY = b'top_30'
TITLE = 'title'
URL = 'url'
BODY = 'body'
SENTENCES = 'sentences'
HACKER_NEWS_ID = 'hn_id'
TEXT = 'text'
APP_ID = os.environ.get('AYLIENID')
APP_KEY = os.environ.get('AYLIENKEY')
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
REDIS_PASS = os.environ.get('REDIS_PASS')