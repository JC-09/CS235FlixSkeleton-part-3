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
    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_User__user_name=username.lower()).one()
        except NoResultFound:
            # Ignore any exception and return None
            pass

        return user

    def get_user_reviews(self, user: User) -> List[Review]:
        check_user = self._session_cm.session.query(User).filter_by(_User__user_name=user.username).one()
        if check_user is not None:
            return list(user.reviews)
        return None

    def add_actor(self, actor: Actor):
        with self._session_cm as scm:
            scm.session.add(actor)
            scm.commit()

    def get_actor(self, actor_full_name) -> Actor:
        actor_fullname = actor_full_name.strip()
        name_list = actor_fullname.split()
        actor_fullname = ''
        for name in name_list:
            name = name.capitalize()
            actor_fullname += name + ' '
        actor_fullname = actor_fullname.strip()
        actor = None
        try:
            actor = self._session_cm.session.query(Actor).filter_by(_Actor__actor_full_name=actor_fullname).one()
        except NoResultFound:
            pass

        return actor

    def check_actor_existence_in_repo(self, actor:Actor) -> bool:
        if isinstance(actor, Actor):
            all_actors = list(self._session_cm.session.query(Actor).all())
            if actor in all_actors:
                return True
        return False

    def get_actor_colleague(self, actor:Actor) -> List[Actor]:
        all_actors = list(self._session_cm.session.query(Actor).all())
        if actor in all_actors:
            return actor.actor_colleague
        return None

    def get_total_number_of_actors(self) -> int:
        return self._session_cm.session.query(Actor).count()

    def add_director(self, director:Director):
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def get_director(self, director_full_name) -> Director:
        director_fullname = director_full_name.strip()
        name_list = director_fullname.split()
        director_fullname = ''
        for name in name_list:
            name = name.capitalize()
            director_fullname += name + ' '
        director_fullname = director_fullname.strip()

        director = None
        try:
            director = self._session_cm.session.query(Director).filter_by(_Director__director_full_name=director_fullname).one()
        except NoResultFound:
            pass
        return director

    def check_director_existence_in_repo(self, director:Director):
        if isinstance(director, Director):
            all_directors = list(self._session_cm.session.query(Director).all())
            if director in all_directors:
                return True
        return False

    def get_total_number_of_directors(self) -> int:
        return self._session_cm.session.query(Director).count()

    def add_genre(self, genre:Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_genre(self, genre_name: str) -> Genre:
        genre = None
        try:
            genre = self._session_cm.session.query(Genre).filter_by(_Genre__genre_name=genre_name).one()
        except NoResultFound:
            pass
        return genre

    def get_genres(self) -> List[Genre]:
        return list(self._session_cm.session.query(Genre).all())

    def get_total_number_of_genres_in_repo(self):
        return self._session_cm.session.query(Genre).count()

    def check_genre_existence(self, genre:Genre) -> bool:
        if isinstance(genre, Genre):
            all_genres = list(self._session_cm.session.query(Genre).all())
            if genre in all_genres:
                return True
        return False

    def add_movie(self, movie:Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, title:str, release_year:int):
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter_by(_title=title, _release_year=release_year).one()
        except NoResultFound:
            pass
        return movie

    def get_movies_by_release_year(self, target_year: int) -> List[Movie]:
        if target_year is None:
            movies = list(self._session_cm.session.query(Movie).all())
            return movies
        else:
            movies = list(self._session_cm.session.query(Movie).filter_by(_release_year=target_year).all())
            print(movies)
            return movies

    def get_movies_played_by_an_actor(self, actor_fullname: str):

        actor = self.get_actor(actor_fullname)

        if actor is not None:
            played_movies = [movie for movie in actor.played_movies]
        else:
            played_movies = list()
        return played_movies

    def get_movies_directed_by_a_director(self, director_fullname:str) -> List[Movie]:
        director = self.get_director(director_fullname)

        if director is not None:
            directed_movies = [movie for movie in director.directed_movies]
        else:
            directed_movies = list()
        return directed_movies

    def get_top_6_highest_revenue_movies(self) -> List[Movie]:
        return list(self._session_cm.session.query(Movie).order_by(desc(Movie._revenue)).limit(6))

    def search_movies_by_actor_and_director(self, actor_fullname: str, director_name: str) -> List[Movie]:
        movies_played_by_actor = self.get_movies_played_by_an_actor(actor_fullname=actor_fullname)
        director = self.get_director(director_name)
        output = list()

        if len(movies_played_by_actor) > 0 and director is not None:
            output = [movie for movie in movies_played_by_actor if
                      movie.director == director]
        return output

    def search_movie_by_title(self, title: str) -> List[Movie]:
        return list(self._session_cm.session.query(Movie).filter(Movie._title.like('%{}%'.format(title))).all())

    def get_latest_movie(self):
        return self._session_cm.session.query(Movie).order_by(desc(Movie._release_year)).first()

    def get_oldest_movie(self):
        return self._session_cm.session.query(Movie).order_by(asc(Movie._release_year)).first()

    def get_release_year_of_previous_movie(self, movie: Movie):
        previous_year = None
        prev = self._session_cm.session.query(Movie).filter(Movie._release_year < movie.release_year).order_by(desc(Movie._release_year)).first()

        if prev is not None:
            previous_year = prev.release_year
        return previous_year

    def get_release_year_of_next_movie(self, movie: Movie):
        next_year = None
        nxt = self._session_cm.session.query(Movie).filter(Movie._release_year > movie.release_year).order_by(asc(Movie._release_year)).first()

        if nxt is not None:
            next_year = nxt.release_year
        return next_year

    def get_movie_by_index(self, index:int):
        return self._session_cm.session.query(Movie).filter_by(_id=index).one()

    def get_total_number_of_movies_in_repo(self):
        return self._session_cm.session.query(Movie).count()

    def get_movie_indexes_for_genre(self, genre_name:str):
        # Use native SQL to retrieve movie ids, since there is no mapped class for the movie_genres table
        row = self._session_cm.session.execute('SELECT id from genres WHERE name = :genre_name', {'genre_name': genre_name}).fetchone()

        if row is None:
            # No genre with the genre_name - create an empty list.
            movie_indexes = list()
        else:
            genre_id = row[0]

            # Retrieve movie id of movies associated with the genre.
            movie_indexes = self._session_cm.session.execute(
                'SELECT movie_id FROM movie_genres WHERE genre_id = :genre_id ORDER BY movie_id ASC',
                {'genre_id': genre_id}
            ).fetchall()  # This will be a list of tuples
            movie_indexes = [id[0] for id in movie_indexes]
        return movie_indexes

    def check_movie_existence(self, movie: Movie) -> bool:
        check_movie = self.get_movie(movie.title, movie.release_year)
        if check_movie is not None:
            return True
        return False

    def get_movie_actors(self, movie:Movie) -> List[Actor]:
        if isinstance(movie, Movie):
            if self.check_movie_existence(movie):
                return movie.actors
        return None

    def get_movie_release_year(self, movie: Movie) -> int:
        if self.check_movie_existence(movie):
            return movie.release_year
        return None

    def get_movie_description(self, movie:Movie) -> str:
        if self.check_movie_existence(movie):
            return movie.description
        return None

    def get_movie_director(self, movie:Movie) -> Director:
        if self.check_movie_existence(movie):
            return movie.director
        return None

    def get_movie_reviews(self, movie:Movie):
        if self.check_movie_existence(movie):
            return movie.reviews

    def get_movie_genres(self, movie:Movie) -> List[Genre]:
        if self.check_movie_existence(movie):
            return movie.genres

    def get_movie_runtime_minutes(self, movie:Movie) -> int:
        if self.check_movie_existence(movie):
            return movie.runtime_minutes

    def get_movies_by_index(self, ids_list):
        return list(self._session_cm.session.query(Movie).filter(Movie._id.in_(ids_list)).all())

    def add_review(self, review:Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def get_reviews(self)-> List[Review]:
        return list(self._session_cm.session.query(Review).all())

    def get_total_number_of_reviews(self):
        return self._session_cm.session.query(Review).count()

    def get_user_reviewed_movie(self, username:str) -> List[Movie]:
        user = self.get_user(username=username)
        movies = list()
        if user is not None:
            for current_review in user.reviews:
                movies.append(current_review.movie)
        return movies

    def get_user_interested_genre_from_reviewed_movies(self, reviewed_movies: List[Movie]) -> List[Movie]:
        genre_list = list()
        if len(reviewed_movies) > 0:
            for movie in reviewed_movies:
                for genre in movie.genres:
                    if genre not in genre_list:
                        genre_list.append(genre)
        return genre_list

    def get_top_movie_by_genre(self, genre:Genre) -> Movie:
        movies_classified_by_genre = list(genre.classified_movies)
        movies_classified_by_genre.sort(key=lambda x: x.revenue, reverse=True)
        return movies_classified_by_genre[0]

    def get_suggestion_for_user(self, username: str) -> List[Movie]:
        user_reviewed_movies = self.get_user_reviewed_movie(username)
        user_interested_genres = self.get_user_interested_genre_from_reviewed_movies(user_reviewed_movies)
        suggestion = list()
        if len(user_interested_genres) > 0:
            for genre in user_interested_genres:
                suggested_movie = self.get_top_movie_by_genre(genre)
                if suggested_movie not in suggestion:
                    suggestion.append(suggested_movie)
        return suggestion

    def get_earliest_year(self):
        movie = self.get_oldest_movie()
        if movie is not None:
            return movie.release_year

    def get_latest_year(self):
        movie = self.get_latest_movie()
        if movie is not None:
            return movie.release_year


# ------------------------------------------------------------------
# -------------- Methods for populating the database ---------------
# ------------------------------------------------------------------


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

        movie_data = [movie_key, movie_title, movie_description, movie_director_fullname, release_year, runtime,
                      movie_revenue]
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
        INSERT INTO movies (id, title, description, director, release_year, runtime_minutes, revenue)
        VALUES(?, ?, ?, ?, ?, ?, ?)"""
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

    insert_users = """
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

    # insert_movie_directors = """
    #     INSERT INTO movie_directors(
    #     id, movie_id, director_id)
    #     VALUES(?, ?, ?)"""
    # cursor.executemany(insert_movie_directors, movie_directors_generator())

    connection.commit()
    connection.close()
