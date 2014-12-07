from mock import patch
from tests import get_resource_path


def test_main_route(test_app, fake_redis_store):
    with patch(
            'redis.StrictRedis',
            return_value=fake_redis_store
    ):
        response = test_app.get('/')
        assert response.status_code == 200
        with open(
                get_resource_path('page_example.txt'),
                'r'
        ) as resource:
            assert (response.data.decode('utf-8') ==
                    resource.read())
