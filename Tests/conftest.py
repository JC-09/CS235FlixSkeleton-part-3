import pytest
import os

from CS235Flix import create_app
from CS235Flix.adapters.memory_repository import MemoryRepository, populate
from CS235Flix.adapters import memory_repository



# TEST_DATA_PATH = "../../../adapters/datafiles/"
# TEST_DATA_PATH = "CS235Flix/adapters/datafiles/"   # This is the path to the full 1000 movies
TEST_DATA_PATH = "Tests/data/"  # This is the path to the 10 movies


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING':True,                          # Set to True during testing
        'TEST_DATA_PATH':TEST_DATA_PATH,         # Path for loading test data into the repository
        'WTF_CSRF_ENABLED':False                 # test_client will not send a CSRF token, so disable validation
    })
    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='thorke', password='cLQ^C#oFXloS'):
        return self._client.post(
            'authentication/login',
            data={'username':username, 'password':password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)

