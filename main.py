from constants import REDIS_HOST, REDIS_PORT, REDIS_PASS, get_environment
from flask import Flask, render_template
import redis
from utils import get_stories

app = Flask(__name__)


@app.route('/')
def hn_tldr():
    environment = get_environment()
    r = redis.StrictRedis(
        host=environment[REDIS_HOST],
        port=environment[REDIS_PORT],
        password=environment[REDIS_PASS]
    )
    stories = get_stories(r)
    return render_template('index.html', stories=stories)

if __name__ == '__main__':
    app.run()
