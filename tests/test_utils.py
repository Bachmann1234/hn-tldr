import json
from constants import HACKER_NEWS_ID, TEXT, SENTENCES, URL, TITLE, TOP_STORIES_KEY
from constants import BODY
from utils import get_stories, FAILED_TO_FIND
from mock import patch


def test_get_stories(fake_redis_store):
    assert get_stories(fake_redis_store) == [{HACKER_NEWS_ID: 8712349,
                                              BODY: {TEXT: 'one\ntwo\nthree', SENTENCES: ['one', 'two', 'three']},
                                              URL: 'http://totalurl.com', TITLE: 'I am a title!'},
                                             {HACKER_NEWS_ID: 8712417, BODY: {TEXT: 'four\nfive\nsix',
                                                                              SENTENCES: ['four', 'five', 'six']},
                                              URL: 'http://real.com', TITLE: 'I am a second title!'},
                                             {HACKER_NEWS_ID: 8712277, BODY: {TEXT: 'seven', SENTENCES: []},
                                              URL: 'http://imathingy.com',
                                              TITLE: 'I am a third title!'}]


def test_failed_to_find_story():
    # Perhaps I should do something more than print....
    unfilled_redis = {TOP_STORIES_KEY: json.dumps([1]).encode('utf-8')}
    with patch('builtins.print') as print_fn:
        get_stories(unfilled_redis)
        assert print_fn.called_with(FAILED_TO_FIND.format(1))
