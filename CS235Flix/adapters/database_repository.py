import csv, os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from CS235Flix.domainmodel.model import Actor, Director, Genre, Movie, User, Review
from CS235Flix.adapters.repository import AbstractRepository

genres = None
actors = None
directors = None


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):
    pass


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def movie_record_generator(filename: str):
    for data_row in read_csv_file(filename=filename):
        movie_key = int(data_row[0])
        movie_title = data_row[1]

        try:
            movie_revenue = float(data_row[10])
        except ValueError:
            movie_revenue = 0

        list_of_genre_names = data_row[2].split(',')

        movie_description = data_row[3]

        movie_director_fullname = data_row[4]

        list_of_actor_fullname = data_row[5].split(',')
        list_of_actor_fullname = [name.strip() for name in list_of_actor_fullname]

        release_year = int(data_row[6])

        runtime = int(data_row[7])

        if movie_director_fullname not in directors:
            directors[movie_director_fullname] = list()
        directors[movie_director_fullname].append(movie_key)

        for genre_name in list_of_genre_names:
            if genre_name not in genres:
                genres[genre_name] = list()
            genres[genre_name].append(movie_key)

        for actor_fullname in list_of_actor_fullname:
            if actor_fullname not in actors:
                actors[actor_fullname] = list()
            actors[actor_fullname].append(movie_key)

        movie_data = [movie_key, movie_title, movie_description, release_year, runtime, movie_revenue]
        yield movie_data


def get_genre_records():
    genre_records = list()
    genre_key = 0

    for genre in genres.keys():
        genre_key += 1
        genre_records.append((genre_key, genre))
    return genre_records


def get_actor_records():
    actor_records = list()
    actor_key = 0
    for actor in actors.keys():
        actor_key += 1
        actor_records.append((actor_key, actor))
    return actor_records


def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of CSV file.
        next(reader)

        # Read remaining rows from the CSV file
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row


def get_director_records():
    director_records = list()
    director_key = 0
    for director in directors.keys():
        director_key += 1
        director_records.append((director_key, director))
    return director_records


def movie_genres_generator():
    movie_genres_key = 0
    genre_key = 0

    for genre in genres.keys():
        genre_key += 1
        for movie_key in genres[genre]:
            movie_genres_key += 1
            yield movie_genres_key, movie_key, genre_key


def movie_actors_generator():
    movie_actors_key = 0
    actor_key = 0

    for actor in actors.keys():
        actor_key += 1
        for movie_key in actors[actor]:
            movie_actors_key += 1
            yield movie_actors_key, movie_key, actor_key


def movie_directors_generator():
    movie_directors_key = 0
    director_key = 0

    for director in directors.keys():
        director_key += 1
        for movie_key in directors[director]:
            movie_directors_key += 1
            yield movie_directors_key, movie_key, director_key


def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path: str):
    connection = engine.raw_connection()
    cursor = connection.cursor()

    global genres
    global actors
    global directors

    genres = dict()
    actors = dict()
    directors = dict()

    insert_movies = """
        INSERT INTO movies (id, title, description, release_year, runtime_minutes, revenue)
        VALUES(?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movie_record_generator(os.path.join(data_path, 'movies.csv')))

    insert_genres = """
        INSERT INTO genres(id, name)
        VALUES(?, ?)"""
    cursor.executemany(insert_genres, get_genre_records())

    insert_actors = """
        INSERT INTO actors(id, name)
        VALUES(?, ?)"""
    cursor.executemany(insert_actors, get_actor_records())

    insert_directors = """
        INSERT INTO directors(id, name)
        VALUES(?, ?)"""
    cursor.executemany(insert_directors, get_director_records())

    insert_users ="""
        INSERT INTO users(
        id, username, password)
        VALUES(?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

    insert_reviews = """
        INSERT INTO reviews(
        id, user_id, movie_id, review_text, ratings, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_reviews, generic_generator(os.path.join(data_path, 'reviews.csv')))

    insert_movie_genres = """
        INSERT INTO movie_genres(
        id, movie_id, genre_id)
        VALUES(?, ?, ?)"""
    cursor.executemany(insert_movie_genres, movie_genres_generator())

    insert_movie_actors = """
        INSERT INTO movie_actors(
        id, movie_id, actor_id)
        VALUES(?, ?, ?)"""
    cursor.executemany(insert_movie_actors, movie_actors_generator())

    insert_movie_directors = """
        INSERT INTO movie_directors(
        id, movie_id, director_id)
        VALUES(?, ?, ?)"""
    cursor.executemany(insert_movie_directors, movie_directors_generator())

    connection.commit()
    connection.close()


