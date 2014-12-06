from constants import REDIS_HOST, REDIS_PORT, REDIS_PASS
from flask import Flask, render_template
import redis
from utils import get_stories

app = Flask(__name__)


@app.route('/')
def hn_tldr():
    r = redis.StrictRedis(
        host=REDIS_HOST,
        port=int(REDIS_PORT),
        password=REDIS_PASS
    )
    stories = get_stories(r)
    return render_template('index.html', stories=stories)

if __name__ == '__main__':
    app.run()