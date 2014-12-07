import os


def get_resource_path(relpath):
    here = os.path.abspath(os.path.dirname(__file__))
    fixtures = os.path.abspath(os.path.join(here, u'test_resources'))
    fpath = os.path.join(fixtures, relpath)
    return fpath
