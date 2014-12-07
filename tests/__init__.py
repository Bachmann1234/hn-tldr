import os


def get_resource(relpath, mode='r'):
    here = os.path.abspath(os.path.dirname(__file__))
    fixtures = os.path.abspath(os.path.join(here, u'test_resources'))
    fpath = os.path.join(fixtures, relpath)
    fixture = open(fpath, mode)
    return fixture