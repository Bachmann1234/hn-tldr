import asyncio
import json
import urllib
import aiohttp
import asyncio_redis
from asyncio_redis.encoders import BytesEncoder
from constants import TOP_STORIES_KEY, URL, TITLE, BODY, APP_ID, APP_KEY, REDIS_PORT, REDIS_PASS, REDIS_HOST
import requests

TOP_100_URL = 'https://hacker-news.firebaseio.com/v0/topstories.json'
STORY_URL = 'https://hacker-news.firebaseio.com/v0/item/{}.json'


def top_30_hn_ids():
    return requests.get(TOP_100_URL).json()[:30]


@asyncio.coroutine
def summarize_url(story_id, title, url, redis_connection):
    aylein_url = 'https://api.aylien.com/api/v1/summarize?url={}'
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/x-www-form-urlencoded',
        'X-AYLIEN-TextAPI-Application-ID': APP_ID,
        'X-AYLIEN-TextAPI-Application-Key': APP_KEY
    }
    response = yield from aiohttp.request(
        'GET',
        aylein_url.format(urllib.parse.quote(url)),
        headers=headers
    )
    response_body = yield from response.read()
    response_body = json.loads(response_body.decode('utf-8'))
    yield from redis_connection.set(str(story_id).encode('utf-8'), json.dumps(
        {URL: url,
         TITLE: title,
         BODY: response_body}).encode('utf-8')
    )


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
    connection = yield from asyncio_redis.Connection.create(
        host=REDIS_HOST,
        port=int(REDIS_PORT),
        password=REDIS_PASS.encode('utf-8'),
        encoder=BytesEncoder()
    )
    top_stories = top_30_hn_ids()
    yield from connection.set(TOP_STORIES_KEY, json.dumps(top_stories).encode(u'utf-8'))
    yield from asyncio.gather(*[asyncio.Task(story_url(story_id, connection)) for story_id in top_stories])
    connection.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
