from mock import patch
from tests import get_resource_path


def _compare_expected_to_response(test_app,
                                  fake_redis_store,
                                  route,
                                  expected_path,
                                  expected_response=200):
    with patch(
        'redis.StrictRedis',
        return_value=fake_redis_store
    ):
        response = test_app.get(route)
        with open(
            get_resource_path(expected_path),
            'r'
        ) as expected:
            assert response.status_code == expected_response
            assert (
                "".join(response.data.decode('utf-8').split()) ==
                "".join(expected.read().split())
            )


def test_main_route(test_app, fake_redis_store):
    _compare_expected_to_response(
        test_app,
        fake_redis_store,
        '/',
        'page_example.txt'
    )


def test_rss(test_app, fake_redis_store):
    _compare_expected_to_response(
        test_app,
        fake_redis_store,
        '/feed.atom',
        'rss_example.txt'
    )
