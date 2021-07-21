import os
import unittest.mock

import pytest


def test_true():
    assert True


# how to skip a test
@pytest.mark.skip('will not run this test')
def test_skipped():
    assert False


# how to skip a test on some conditions
@pytest.mark.skipif(True, reason='skip on some condition')
def test_on_condition():
    assert False


# how to skip a test at runtime
def test_skip_at_runtime():
    if True:
        pytest.skip("skip test at runtime")


# how to mark a test
@pytest.mark.slow
def test_slow():
    assert True


@pytest.mark.serial
def test_serial():
    assert True


# use marks not registered will raise an error
# @pytest.mark.unknown
# def test_unknown():
#     assert True
class SimpleDBApp:
    def __init__(self, driver):
        self.driver = driver

    def start(self):
        print('start', self)

    def stop(self):
        print('stop', self)

    def insert(self, *args):
        print('insert', self, args)


@pytest.fixture(scope='module', params=['driver1', 'driver2'])
def simple_database(request):
    db = SimpleDBApp(request.param)
    db.start()
    yield db
    db.stop()


def test_common_object(simple_database):
    simple_database.insert(123)


@pytest.fixture(autouse=True)
def change_user_env():
    env_name = 'USER'
    current_user = os.environ.get(env_name)
    os.environ[env_name] = 'foobar'
    yield
    os.environ[env_name] = current_user


def test_user():
    env_name = 'USER'
    assert os.getenv(env_name) == 'foobar'


def test_mock():
    def fake_os_unlink(path):
        raise IOError('Testing!')
    with unittest.mock.patch('os.unlink', fake_os_unlink):
        with pytest.raises(IOError):
            os.unlink('foobar')


