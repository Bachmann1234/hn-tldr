from blessings import Terminal
from constants import TITLE, URL, BODY, SENTENCES, REDIS_PASS, REDIS_PORT, REDIS_HOST
import redis
from utils import get_stories


def format_response(response):
    t = Terminal()
    print(t.bold("{} - {}".format(response[TITLE], response[URL])))
    for line in response[BODY][SENTENCES]:
        print("* {}".format(line))
    print("-" * 25)
    print("\n")


if __name__ == '__main__':
    """
    assumes you populated the cache
    """
    r = redis.StrictRedis(
        host=REDIS_HOST,
        port=int(REDIS_PORT),
        password=REDIS_PASS
    )

    list(map(format_response, get_stories(r)))