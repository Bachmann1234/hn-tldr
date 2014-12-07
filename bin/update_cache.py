#!/usr/bin/env python
import asyncio
import json
import urllib
import aiohttp
import asyncio_redis
from asyncio_redis.encoders import BytesEncoder
from constants import TOP_STORIES_KEY, URL, TITLE, BODY, REDIS_PORT, REDIS_PASS, REDIS_HOST, \
    get_environment, AYLIEN_ID, AYLIEN_KEY
import requests

TOP_100_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
STORY_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'


def top_30_hn_ids():
    return requests.get(TOP_100_URL).json()[:30]


@asyncio.coroutine
def summarize_url(story_id, title, url, redis_connection):
    environment = get_environment()
    aylein_url = 'https://api.aylien.com/api/v1/summarize?url={}'
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/x-www-form-urlencoded',
        'X-AYLIEN-TextAPI-Application-ID': environment[AYLIEN_ID],
        'X-AYLIEN-TextAPI-Application-Key': environment[AYLIEN_KEY]
    }
    response = yield from aiohttp.request(
        'GET',
        aylein_url.format(urllib.parse.quote(url)),
        headers=headers
    )
    response_body = yield from response.read()
    response_body = json.loads(response_body.decode('utf-8'))
    redis_key = str(story_id).encode('utf-8')
    yield from redis_connection.set(redis_key, json.dumps(
        {URL: url,
         TITLE: title,
         BODY: response_body}).encode('utf-8')
    )
    yield from redis_connection.expire(redis_key, (60 * 60 * 24 * 3))  # Expire after 3 days


@asyncio.coroutine
def story_url(story_id, redis_connection):
    response = yield from aiohttp.request('GET', STORY_URL.format(story_id))
    if response.status == 200:
        body = yield from response.read()
        body = json.loads(body.decode('utf-8'))
        url = body[URL]
        title = body[TITLE]
        if url:
            response = yield from redis_connection.get(str(story_id).encode('utf-8'))
            if not response:
                yield from summarize_url(story_id, title, url, redis_connection)
    else:
        print("Failed to get story: {}".format(story_id))


def main():
    environment = get_environment()
    connection = yield from asyncio_redis.Connection.create(
        host=environment[REDIS_HOST],
        port=environment[REDIS_PORT],
        password=environment[REDIS_PASS].encode('utf-8'),
        encoder=BytesEncoder()
    )
    top_stories = top_30_hn_ids()
    yield from connection.set(TOP_STORIES_KEY, json.dumps(top_stories).encode(u'utf-8'))
    yield from asyncio.gather(*[asyncio.Task(story_url(story_id, connection)) for story_id in top_stories])
    connection.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
