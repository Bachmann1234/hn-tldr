from datetime import datetime
from urllib.parse import urljoin
from constants import REDIS_HOST, REDIS_PORT, REDIS_PASS, get_environment, URL, TITLE, SENTENCES, BODY, DATE_FOUND, \
    HACKER_NEWS_ID
from flask import Flask, render_template, request
import redis
from utils import get_stories
from werkzeug.contrib.atom import AtomFeed

app = Flask(__name__)


def _get_stories():
    environment = get_environment()
    r = redis.StrictRedis(
        host=environment[REDIS_HOST],
        port=environment[REDIS_PORT],
        password=environment[REDIS_PASS]
    )
    return get_stories(r)


@app.route('/feed.atom')
def rss():
    feed = AtomFeed('Hacker News TLDR',
                    feed_url=request.url, url=request.url_root)
    stories = _get_stories()
    for story in stories:
        if not story.get(BODY, {}).get(SENTENCES):
            body = 'Unable to generate summary'
        else:
            body = '<ul>{}</ul>'.format(
                '\n'.join(
                    "<li>{}</li>".format(
                        sentence
                    ) for sentence in story[BODY][SENTENCES]
                )
            )
            body += "<br/><a href={}>HN Comments</a>".format(
                'https://news.ycombinator.com/item?id={}'.format(
                    story[HACKER_NEWS_ID]
                )
            )
        feed.add(story[TITLE], body,
                 content_type='html',
                 updated=datetime.strptime(story[DATE_FOUND], '%Y-%m-%d %H:%M:%S.%f'),
                 url=urljoin(request.url_root, story[URL]),
                 )
    return feed.get_response()


@app.route('/')
def hn_tldr():
    return render_template('index.html', stories=_get_stories())

if __name__ == '__main__':
    app.run(debug=True)
