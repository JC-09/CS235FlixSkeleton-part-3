# CS235Flix/movies/services.py

from typing import List, Iterable
from CS235Flix.adapters.repository import AbstractRepository
from CS235Flix.domainmodel.model import Movie, Review, Genre, make_review, Actor, Director


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class NonExistentActorException(Exception):
    pass


class NonExistentDirectorException(Exception):
    pass


class NoSearchResultsException(Exception):
    pass


def add_review(review_text: str, username: str, movie_id: int, rating: int, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie_by_index(movie_id)
    if movie is None:
        raise NonExistentMovieException

    # Check that the user exists
    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create review
    review = make_review(review_text=review_text, user=user, movie=movie, rating=rating)

    # Update the repository
    repo.add_review(review)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie_by_index(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)


def get_latest_movie(repo: AbstractRepository):
    movie = repo.get_latest_movie()

    return movie_to_dict(movie)


def get_oldest_movie(repo: AbstractRepository):
    movie = repo.get_oldest_movie()
    return movie_to_dict(movie)


def get_movies_by_release_year(year, repo: AbstractRepository):
    movies = repo.get_movies_by_release_year(target_year=year)

    movies_dto = list()
    prev_year = next_year = None
    if len(movies) > 0:
        prev_year = repo.get_release_year_of_previous_movie(movies[0])
        next_year = repo.get_release_year_of_next_movie(movies[0])

        # Convert Movies to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto, prev_year, next_year


def get_movie_ids_for_genre(genre_name: str, repo: AbstractRepository):
    movie_ids = repo.get_movie_indexes_for_genre(genre_name)

    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_index(id_list)

    # Convert Movies to dictionary form
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie_by_index(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews)


def search_movie_by_actor_fullname(actor_fullname: str, repo: AbstractRepository):

    movies = repo.get_movies_played_by_an_actor(actor_fullname=actor_fullname)
    if len(movies) == 0:
        raise NonExistentActorException

    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def search_movie_directed_by_director_fullname(director_fullname: str, repo: AbstractRepository):
    movies = repo.get_movies_directed_by_a_director(director_fullname=director_fullname)
    if len(movies) == 0:
        raise NonExistentDirectorException
    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def search_movie_by_actor_and_director(actor_fullname: str, director_fullname: str, repo: AbstractRepository):
    movies = repo.search_movies_by_actor_and_director(actor_fullname=actor_fullname,
                                                      director_fullname=director_fullname)
    if len(movies) == 0:
        raise NoSearchResultsException

    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def search_movie_by_title(title:str, repo:AbstractRepository):
    movies = repo.search_movie_by_title(title)
    if len(movies) == 0:
        raise NoSearchResultsException

    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def get_top_6_movies_by_revenue(repo:AbstractRepository):
    movies = repo.get_top_6_highest_revenue_movies()
    if len(movies) == 0:
        raise NoSearchResultsException

    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict


def get_suggestions_for_a_user(username: str, repo: AbstractRepository):
    movies = repo.get_suggestion_for_user(username=username)
    movies_as_dict = movies_to_dict(movies)
    return movies_as_dict

# ============================================
# Functions to convert model entities to dicts
# ============================================


def movie_to_dict(movie: Movie):
    movie_dict = {
        'id': movie.id,
        'title': movie.title,
        'release_year': movie.release_year,
        'description': movie.description,
        'director': movie.director.director_full_name,
        'actors': actors_to_dict(movie.actors),
        'genres': genres_to_dict(movie.genres),
        'runtime_minutes': movie.runtime_minutes,
        'reviews': reviews_to_dict(movie.reviews),
        'revenue': movie.revenue
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def actor_to_dict(actor: Actor):
    actor_dict = {
        'actor_fullname': actor.actor_full_name
    }
    return actor_dict


def actors_to_dict(actors: Iterable[Actor]):
    return [actor_to_dict(actor) for actor in actors]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'genre_name': genre.genre_name,
        'number_of_classified_movies': genre.number_of_classified_movies,
        'classified_movies': [movie.id for movie in genre.classified_movies]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


def review_to_dict(review: Review):
    review_dict = {
        'username': review.review_author.username,
        'movie_id': review.movie.id,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


# ============================================
# Functions to convert dicts to model entities
# ============================================


def dict_to_movie(dict):
    movie = Movie(dict['title'], dict['release_year'], dict['id'])

    # There is no actors, director, genres, reviews, nor runtime_minutes
    return movie
