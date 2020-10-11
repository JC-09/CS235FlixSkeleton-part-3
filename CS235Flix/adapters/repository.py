import abc
from typing import List
from CS235Flix.domainmodel.model import User, Actor, Director, Genre, Movie, Review, WatchList

repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """ Adds a User to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """
            Returns the User named username from the repository.
            If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_watched_movies(self, user:User) -> List[Movie]:
        """ Returns a list of movies that had been watched by the given user
            Returns None if the given user does not exist in the repository
            Returns an empyt list of the given user has not watched any movies yet
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_reviews(self, user:User) -> List[Review]:
        """ Returns a list of reviews made by the given User.
            This method returns None if the given user does not exist in the repository
            This method returns an empty list if the given user has not made any reviews yet
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_time_spent_watching_movies_minutes(self, user:User):
        """ Returns the total time (in minutes) the user spent on watching movies
            This method returns None if the given user does not exist in the repository
        """
        raise NotImplementedError


    @abc.abstractmethod
    def add_actor(self, actor:Actor):
        """ Adds an actor to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_full_name) -> Actor:
        """ Returns an Actor with the full name of actor_full_name
            If there is no Actor with the given full name, this method returns None
        """
        raise NotImplementedError

    def check_actor_existence_in_repo(self, actor:Actor) -> bool:
        """ Checks if an actor exist in the repository
            Returns True if so, otherwise, return false
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor_colleague(self, actor:Actor) -> List[Actor]:
        """
            Returns a list of colleagues of the actor with full name as actor_full_name
            This method returns None if there is no Actor with the name actor_full_name, and
            returns an empty list if the actor has no colleague.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_total_number_of_actors(self) -> int:
        """ Returns the number of Actors in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director:Director):
        """ Adds a director to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_full_name) -> Director:
        """ Returns a Director with the director full name = director_full_name.
            If no director in the repository is with the given fullname, this method returns None.
        """

    @abc.abstractmethod
    def check_director_existence_in_repo(self, director:Director):
        """ Return True if the given director exist in the repo, otherwise return false"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_total_number_of_directors(self) -> int:
        """ Returns the total number directors in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre:Genre):
        """ Adds a genre to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the genres stored in the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_total_number_of_genres_in_repo(self):
        """ Returns the total number of (unique) genres in repo """
        raise NotImplementedError

    @abc.abstractmethod
    def check_genre_existence(self, genre:Genre) -> bool:
        """ Return True if the given genre exist in the repository, return False otherwise"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie:Movie):
        """ Adds a movie to the repository and add the index of movie to repo"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, title:str, release_year:int):
        """ Returns a Movie with the given title AND release_year
            If no movie in the repository has the given title AND release_year, this method
            returns None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_release_year(self, target_year: int) -> List[Movie]:
        """ Return a list of Movies tha were released in the target_year

            If there are no Movies on the given year, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_played_by_an_actor(self, actor_fullname:str) -> List[Movie]:
        """ Returns a list of movies played by the actor.
            Returns an empty list if the supplied actor does not exist or the actor hasn't played any movie
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_directed_by_a_director(self, director_fullname:str) -> List[Movie]:
        """ Returns a list of movies directed by the director
            Returns an empty list of the supplied directed does not exist or the director didn't direct any movie
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_top_6_highest_revenue_movies(self) -> List[Movie]:
        """ Returns a list of the top 5 highest revenue movies in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def search_movies_by_actor_and_director(self, actor_fullname: str, director_name: str):
        """ Returns a list of movies played by a specific actor AND directed by the specific director
            Returns an empty list when the search criteria returns nothing
        """
        raise NotImplementedError


    @abc.abstractmethod
    def search_movie_by_title(self, title: str) -> List[Movie]:
        """ Returns a list of movies that matches the title
            Returns an empty list if no matched movie title found
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_latest_movie(self):
        """ Return the latest Movie, ordered by release year, from the repository.
            Returns None if the repository is empty
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_oldest_movie(self):
        """Return the oldest Movie, ordered by release year, from the repository
            Returns None if the repository is empty
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_release_year_of_previous_movie(self, movie: Movie):
        """ Returns the release year of a Movie that immediately precedes movie.
            If movie is the first Movie in the repository, this method returns none because there are no Movies
            in the previous year.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_release_year_of_next_movie(self, movie: Movie):
        """ Returns the release year of a Movie that immediately after movie.
            If movie is the first Movie in the repository, this method returns none because there are no Movies
            in the previous year.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_total_number_of_movies_in_repo(self):
        """ Returns the total number of movies in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_index(self, index:int):
        """ Returns a Movie with the given index
            Returns None if the movie does not exist in the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_indexes_for_genre(self, genre_name:str):
        """ Returns a list of movie indexes representing Movies that are classified by the given genre_name
            If there are no movie are classified by the given genre name then the method returns an empty list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_actors(self, movie:Movie) -> List[Actor]:
        """ Returns a list of Actors acted in the given Movie
            If the given movie does not exist in the repository, this method returns None
            If the given movie does not have any actor, this method returns an empty list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_release_year(self, movie:Movie) -> int:
        """ Returns the release year of the given movie
            Returns None if the given movie not exist in the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_description(self, movie:Movie) -> str:
        """ Returns the description of the given movie.
            This method returns None if the given movie does not exist in the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_director(self, movie:Movie) -> Director:
        """ Returns the Director of the given Movie
            This method returns None if the given Movie does not exist in the Repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_reviews(self, movie:Movie):
        """ Returns a list of reviews of the given movie """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_genres(self, movie:Movie) -> List[Genre]:
        """ This method returns the list of genres of the given Movie
            This method returns None if the given Movie does not exist in the repository
            This method returns an empty list if the given Movie does not have any genres
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_runtime_minutes(self, movie:Movie) -> int:
        """ Returns the runtime minutes of the given Movie
            This method returns None if the given movie does not exist in the repository
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_index(self, ids_list):
        """ Returns a list of Movies, whose index match those in ids_list, from the repository "
            If there are no matches, this method returns an empty list
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review:Review):
        """ Adds a Review to the repository

            If the review doesn't have bidrectional links with a Movie and a User, this method raises a
            RepositoryException and doesn't update the repository
        """
        if review.review_author is None or review not in review.review_author.reviews:
            raise RepositoryException("Review not correctly attached to a User")
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException("Review not correctly attached to a Movie")

    @abc.abstractmethod
    def get_reviews(self) -> List[Review]:
        """ Returns reviews stored in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_total_number_of_reviews(self) -> int:
        """ Returns the total number of reviews stored in the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def add_watchlist(self, watchlist:WatchList):
        """ Adds an empty watchlist to the repository """
        raise NotImplementedError

    @abc.abstractmethod
    def get_watchlist(self) -> List[WatchList]:
        """ Returns a list of watchlist in the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_reviewed_movie(self, username:str) -> List[Movie]:
        """ Returns a list of movies reviewed by the login user
            If a user is not logged in, the web application will redirect the user to login
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user_interested_genre_from_reviewed_movies(self, reviewed_movies: List[Movie]) -> List[Movie]:
        """ Returns a list of genres based on the user's reviewed movie.
            Returns an empty list of the input list is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_top_movie_by_genre(self, genre:Genre) -> Movie:
        """ Returnes a movie with the highest revenue classified by the genre """
        raise NotImplementedError

    @abc.abstractmethod
    def get_suggestion_for_user(self, username: str) -> List[Movie]:
        """ Returns a list of movies recommend for the user
        """
        raise NotImplementedError