import pytest

from flask import session


def test_register(client):  # Test the register method in authentication.py
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid username and password.
    response = client.post(
        '/authentication/register',
        data={'username': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(
    ('username', 'password', 'message'),(
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contains an upper case letter, a lower case letter, and a digit'),
        ('fmercury', 'Test#6^0', b'Your username is already taken - please try another'),
    ))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username
    # and password generate appropriate error messages
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):  # Test the login method in authentication.py
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage
    response = auth.login()
    assert response.headers['Location'] == "http://localhost/suggest"

    # Check that a session has been created for the logged-in user
    with client:
        client.get('/')
        assert session['username'] == 'thorke'


def test_logout(client, auth):
    # Login a user
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'CS235' in response.data


def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page
    response = client.get('/review?movie=1')
    response = client.post(
        '/review',
        data={'review': 'what a great movie!', 'rating': 10, 'movie_id': 1}
    )
    assert response.headers['Location'] == 'http://localhost/search_movies_by_title?title=Guardians+of+the+Galaxy'


@pytest.mark.parametrize(('review', 'rating', 'messages'), (
        ('This movie is fucking awesome!','9', (b'Your review must not contain profanity')),
        ('Hey', '5', (b'Your review is too short')),
        ('ass', '1', (b'Your review is too short', b'Your review must not contain profanity')),
        ('I love it!', '', (b'Please leave a rating from 1 to 10')),
        ('I love it!', 'A+', (b'You must enter a number')),
))
def test_review_with_invalid_input(client, auth, review, rating, messages):
    # Login a user.
    auth.login()

    # Attempt to comment on an article
    response = client.post(
        '/review',
        data={'review': review, 'movie_id': 1}
    )

    # Check that supplying invalid review text or not leaving a rating generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_movie_without_year(client):
    # Check that we can retrieve the movies page.
    response = client.get('/movies_by_release_year')
    assert response.status_code == 200

    # Check that without providing a release year query parameter the page includes the latest movie
    assert b'The Lost City of Z' in response.data
    assert b'Passengers' in response.data
    assert b'Guardians of the Galaxy' not in response.data


def test_movies_with_release_year(client):
    # Check that we can retrieve the movies page. movies_by_release_year?year=2013
    response = client.get('/movies_by_release_year?year=2014')
    assert response.status_code == 200

    assert b'Guardians of the Galaxy' in response.data
    assert b'Prisoners' not in response.data


def test_movies_with_review(client):
    # Check that we can retrieve the movies page:
    response = client.get('/movies_by_release_year?year=2014&view_reviews_for=1')
    assert response.status_code == 200

    # Check that all comments for specified article are included on the page
    assert b'This movie is great!' in response.data
    assert b'This movie is awesome' in response.data
    assert b'Love it!' in response.data


def test_movies_with_genre(client):
    # Check that we can retrieve the movie page
    response = client.get('/movies_by_genre?genre=Horror')
    assert response.status_code == 200

    # Check that all movies classified as 'Horror' are returned back
    assert b'Split' in response.data
    assert b"Don't Breathe" not in response.data  # The movie "Don't Breathe" is classified as Horror, but it is not in the testing data


def test_search_by_actor_fullname(client):
    # Check that we can search movies by an actor fullname
    response = client.post('/search', data={'actor': "Chris Pratt"})
    assert response.headers['Location'] == "http://localhost/search_movies_by_actor_and_or_director?actor=Chris+Pratt&director="

    # Check that we have the desired results returned by the search
    response = client.get('/search_movies_by_actor_and_or_director?actor=Chris+Pratt&director=')
    assert response.status_code == 200
    assert b'Guardians of the Galaxy' in response.data
    assert b'Passengers' in response.data


def test_search_by_director_fullname(client):
    # Check that we can search movies by director fullname
    response = client.post('/search', data={'director': 'Christophe Lourdelet'})
    assert response.headers['Location'] == 'http://localhost/search_movies_by_actor_and_or_director?actor=&director=Christophe+Lourdelet'

    response = client.get('/search_movies_by_actor_and_or_director?actor=&director=Christophe+Lourdelet')
    assert response.status_code == 200
    assert b'Sing' in response.data


def test_search_by_actor_and_director(client):
    # Check that we can search by actor and director fullname
    response = client.post('/search', data={'actor': 'Chris Pratt', "director": "James Gunn"})
    assert response.headers['Location'] == 'http://localhost/search_movies_by_actor_and_or_director?actor=Chris+Pratt&director=James+Gunn'

    # Check that we have the desired movie returned by the search
    response = client.get('/search_movies_by_actor_and_or_director?actor=Chris+Pratt&director=James+Gunn')
    assert response.status_code == 200
    assert b'Guardians of the Galaxy' in response.data


def test_search_by_movie_title(client):
    # Check that we can search by movie title:
    response = client.post('/search_by_title', data={'title': "Passengers"})
    assert response.headers['Location'] == 'http://localhost/search_movies_by_title?title=Passengers'

    # Check that we can have the desired movie returned by the search
    response = client.get('/search_movies_by_title?title=Passengers')
    assert response.status_code == 200
    assert b'Passengers' in response.data
    assert b'2016' in response.data


def test_can_suggest_movies_to_a_logged_in_user(client, auth):
    # Login a user
    auth.login()

    # Check that we can retrieve suggestions for the logged in user:
    response = client.get('/suggest')
    assert response.status_code == 200

    # Check that we a desired movie is returned
    assert b'Guardians of the Galaxy' in response.data


def test_repository_will_not_suggest_movies_un_logged_in_user(client):
    # Check that we can retrieve suggestions for the logged in user:
    response = client.get('/suggest')
    assert response.headers['Location'] == 'http://localhost/authentication/login'