import json
from constants import TOP_STORIES_KEY, HACKER_NEWS_ID


def get_stories(redis_connection):
    stories = []
    for story_id in json.loads(redis_connection.get(TOP_STORIES_KEY).decode('utf-8')):
        response = redis_connection.get(str(story_id).encode('utf-8'))
        if not response:
            print("Failed to find story {}".format(story_id))
        else:
            story = json.loads(response.decode('utf-8'))
            story[HACKER_NEWS_ID] = story_id
            stories.append(story)
    return stories
