import pytest

import datetime
from sqlalchemy.exc import IntegrityError

from CS235Flix.domainmodel.model import (User, Movie, Actor, Director, Review, Genre,
                                         make_review, make_movie_genre_association, make_movie_actor_association)

review_date = datetime.date(2020, 10, 23)


def insert_user(empty_session, values=None):
    new_name = 'Andrew'
    new_password = '1234'

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users(username, password) VALUES(:username, :password)',
                          {'username': new_name, 'password': new_password})

    row = empty_session.execute('SELECT id from users where username = :username',
                                {'username': new_name}).fetchone()

    return row[0]  # returns the auto-incremented user id


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users(username, password) VALUES(:username, :password)',
                              {'username': value[0], 'password': value[1]})

    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys


def make_movie():
    movie = Movie('Avengers: Endgame', 2019)
    movie.set_director(Director("Anthony Russo"))
    movie.set_description("After Thanos, an intergalactic warlord, disintegrates half of the universe, the Avengers must reunite and assemble again to reinvigorate their trounced allies and restore balance.")
    movie.set_runtime_minutes(181)
    return movie


def make_user():
    user = User('andrew', '1234')
    return user


def make_genre():
    genre = Genre('Testing Genre')
    return genre


def make_actor():
    actor = Actor("Robert Downey Jr.")
    return actor


def insert_reviewed_movie(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    rating_1 = 10
    rating_2 = 8

    empty_session.execute(
        'INSERT INTO reviews (user_id, movie_id, review_text, ratings, timestamp) VALUES '
        '(:user_id, :movie_id, "review 1", :rating_1, :timestamp_1),'
        '(:user_id, :movie_id, "review 2", :rating_2, :timestamp_2)',
        {'user_id': user_key, 'movie_id': movie_key, 'rating_1': rating_1, 'rating_2': rating_2,
         'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id FROM movies').fetchone()
    return row[0]


def insert_movie(empty_session):
    empty_session.execute(
        'INSERT INTO movies (title, description, director, release_year, runtime_minutes) VALUES'
        '("Avengers: Endgame", "After Thanos, an intergalactic warlord, disintegrates half of the universe, the Avengers must reunite and assemble again to reinvigorate their trounced allies and restore balance."'
        ', "Joe Russo", :release_year, :runtime_minutes)', {'release_year': 2019, 'runtime_minutes': 181}
    )

    row = empty_session.execute('SELECT id from movies').fetchone()
    return row[0]  # return movie id


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (name) VALUES("Test_1"), ("Test_2")'
    )
    rows = list(empty_session.execute('SELECT id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_actors(empty_session):
    empty_session.execute(
        'INSERT INTO actors (name) VALUES ("Robert Downey Jr"), ("Chris Evans")'
    )
    rows = list(empty_session.execute('SELECT id from actors'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_movie_actor_association(empty_session, movie_key, actor_keys):
    stmt = 'INSERT INTO movie_actors(movie_id, actor_id) VALUES(:movie_id, :actor_id)'
    for actor_key in actor_keys:
        empty_session.execute(stmt, {'movie_id': movie_key, 'actor_id': actor_key})


def insert_movie_genre_association(empty_session, movie_key, genre_keys):
    stmt = 'INSERT INTO movie_genres(movie_id, genre_id) VALUES(:movie_id, :genre_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'movie_id': movie_key, 'genre_id': genre_key})


def test_saving_of_users_with_common_username(empty_session):
    insert_user(empty_session, ('andrew', '1234'))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("andrew", "111")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_users(empty_session):
    users = list()
    users.append(("andrew", "1234"))
    users.append(("cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("andrew", "1234"),
        User("cindy", "999")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("andrew", "1234")]


def test_loading_of_movie(empty_session):
    movie_key = insert_movie(empty_session)
    expected_movie = make_movie()
    fetched_movie = empty_session.query(Movie).one()

    assert expected_movie == fetched_movie
    assert movie_key == fetched_movie.id


def test_saving_of_movie(empty_session):
    movie = make_movie()
    empty_session.add(movie)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, title, description, director, release_year, runtime_minutes, revenue FROM movies'))
    assert rows == [(1, 'Avengers: Endgame',
                     "After Thanos, an intergalactic warlord, disintegrates half of the universe, the Avengers must reunite and assemble again to reinvigorate their trounced allies and restore balance.",
                     "Anthony Russo",
                     2019,
                     181,
                     0.0
                     )]


def test_loading_of_classified_movie(empty_session):
    movie_key = insert_movie(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_movie_genre_association(empty_session, movie_key, genre_keys)

    movie = empty_session.query(Movie).get(movie_key)
    genres = [empty_session.query(Genre).get(key) for key in genre_keys]

    for genre in genres:
        assert movie.is_classified_as(genre)
        assert genre.is_applied_to(movie)


def test_saving_classified_movie(empty_session):
    movie = make_movie()
    genre = make_genre()

    # Establish the bidirectional relationship between the Movie and the Genre
    make_movie_genre_association(movie=movie, genre=genre)

    # Persist the Movie and Genre
    # Note: it doesn't matter whether we add the Genre or the Movie. They are connected bi-directionally
    # So persisting either one will persist the other.
    empty_session.add(movie)
    empty_session.commit()

    # Test test_saving_of_movie() checks for the insertion into the movies table.
    rows = list(empty_session.execute('SELECT id FROM movies'))
    movie_key = rows[0][0]

    # Check that the genres table has a new record.
    rows = list(empty_session.execute('SELECT id, name FROM genres'))
    genre_key = rows[0][0]
    assert rows[0][1] == 'Testing Genre'

    # Check that the movie_genres table has a new record
    rows = list(empty_session.execute('SELECT movie_id, genre_id FROM movie_genres'))
    movie_foreign_key = rows[0][0]
    genre_foreign_key = rows[0][1]

    assert movie_key == movie_foreign_key
    assert genre_key == genre_foreign_key


def test_loading_of_reviewed_movie(empty_session):
    insert_reviewed_movie(empty_session)

    rows = empty_session.query(Movie).all()

    movie = rows[0]

    assert len(list(movie.reviews)) == 2

    for review in movie.reviews:
        assert review.movie is movie


def test_saving_of_review(empty_session):
    movie_key = insert_movie(empty_session)
    user_key = insert_user(empty_session)

    rows = empty_session.query(Movie).all()

    movie = rows[0]
    user = empty_session.query(User).all()[0]

    # Create a new review that is bidirectionally linked with the User and the Movie
    review_text = "Some review text"
    rating = 6

    review = make_review(review_text=review_text, user=user, movie=movie, rating=rating)

    # Note: if the bidirectional links between the new Review and the User and
    # Article objects hadn't been established in memory, they would exist following
    # committing the addition of the Review to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, movie_id, review_text FROM reviews'))
    assert rows == [(user_key, movie_key, review_text)]


def test_save_reviewed_movie(empty_session):
    # Create Movie User objects.
    movie = make_movie()
    user = make_user()

    # Create a new Review that is bidirectionally linked with the User and the Movie
    review_text = 'Some review text.'
    review = make_review(review_text=review_text, user=user, movie=movie, rating=10)

    # Save the new Movie
    empty_session.add(movie)
    empty_session.commit()

    # Test test_saving_of_movie() checks for insertion into the movies table
    rows = list(empty_session.execute('SELECT id FROM movies'))
    movie_key = rows[0][0]

    # Test test_saving_of_users() checks for the insertion into the users table
    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    # Check that the reviews table has a new record that links to the movies and users tables.
    rows = list(empty_session.execute('SELECT user_id, movie_id, review_text FROM reviews'))
    assert rows == [(user_key, movie_key, review_text)]


# Test actors related functions
def test_loading_of_played_movie(empty_session):
    movie_key = insert_movie(empty_session)
    actor_keys = insert_actors(empty_session)
    insert_movie_actor_association(empty_session, movie_key, actor_keys)

    movie = empty_session.query(Movie).get(movie_key)
    actors = [empty_session.query(Actor).get(key) for key in actor_keys]

    for actor in actors:
        assert movie in list(actor.played_movies)
        assert actor in list(movie.actors)


def test_saving_played_movie(empty_session):
    movie = make_movie()
    actor = make_actor()

    # Establish the bidirectional relationship between the Movie and the Actor
    make_movie_actor_association(movie, actor)

    # Persist the Movie and Actor
    # Note: it doesn't matter whether we add the Actor or the Movie. They are connected bi-directionally
    # So persisting either one will persist the other.
    empty_session.add(movie)
    empty_session.commit()

    # Test test_saving_of_movie() checks for the insertion into the movies table
    rows = list(empty_session.execute('SELECT id FROM movies'))
    movie_key = rows[0][0]
    print("movie_key = " + str(movie_key))
    # Check that movies table has a new record.
    rows = list(empty_session.execute('SELECT id, name FROM actors'))
    actor_key = rows[0][0]
    assert rows[0][1] == "Robert Downey Jr."
    print('actor_key = ' + str(actor_key))
    # Check that the movie_actors table has a new record
    rows = list(empty_session.execute('SELECT movie_id, actor_id FROM movie_actors'))
    print(rows)
    movie_foreign_key = rows[0][0]
    actor_foreign_key = rows[0][1]

    assert movie_key == movie_foreign_key
    assert actor_key == actor_foreign_key















