from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime, Float,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship
import datetime
from CS235Flix.domainmodel import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review_text', String(1024), nullable=False),
    Column('ratings', Integer, nullable=False),
    Column('timestamp', Date, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    Column('director', ForeignKey('directors.name')),
    Column('release_year', Integer, nullable=False),
    Column('runtime_minutes', Integer, nullable=False),
    Column('revenue', Float, nullable=True, default=0.0),
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False),
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False),
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)


movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('actor_id', ForeignKey('actors.id'))
)


# movie_directors = Table(
#     'movie_directors', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('movie_id', ForeignKey('movies.id')),
#     Column('director_id', ForeignKey('directors.id'))
# )


def map_model_to_tables():
    mapper(
        model.User, users, properties={
            '_User__user_name': users.c.username,
            '_User__password': users.c.password,
            '_User__reviews': relationship(model.Review, backref='_Review__author')
        }
    )

    mapper(
        model.Review, reviews, properties={
            '_Review__review_text': reviews.c.review_text,
            '_Review__rating': reviews.c.ratings,
            '_Review__timestamp': reviews.c.timestamp
        }
    )

    movies_mapper = mapper(
        model.Movie, movies, properties={
            '_id': movies.c.id,
            '_title': movies.c.title,
            '_Movie__description': movies.c.description,
            '_Movie__director__director_full_name': movies.c.director,
            '_release_year': movies.c.release_year,
            '_Movie__runtime_minutes': movies.c.runtime_minutes,
            '_revenue': movies.c.revenue,
            '_Movie__reviews': relationship(model.Review, backref='_Review__movie')
        }
    )

    mapper(model.Director, directors, properties={
        '_Director__director_full_name': directors.c.name,
        '_Director__directed_movies': relationship(model.Movie, backref='_Movie__director')
    })

    mapper(model.Actor, actors, properties={
        '_Actor__actor_full_name': actors.c.name,
        '_Actor__played_movies': relationship(
            movies_mapper,
            secondary=movie_actors,
            backref='_Movie__actors'
        )
    })

    mapper(model.Genre, genres, properties={
        '_Genre__genre_name': genres.c.name,
        '_Genre__classified_movies': relationship(
            movies_mapper,
            secondary=movie_genres,
            backref='_Movie__genres'
        )
    })











