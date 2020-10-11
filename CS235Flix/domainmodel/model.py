from datetime import datetime
from typing import List
# import imdb

class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
            self.__actor_colleague = list()
            self.__played_movies = list()
        else:
            self.__actor_full_name = actor_full_name.strip()
            self.__actor_colleague = list()
            self.__played_movies = list()

    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @property
    def actor_colleague(self):
        return iter(self.__actor_colleague)

    @property
    def played_movies(self):
        return iter(self.__played_movies)

    def add_actor_colleague(self, colleague):
        if isinstance(colleague, Actor):
            self.__actor_colleague.append(colleague)
            colleague.__actor_colleague.append(self)

    def add_played_movies(self, movie):
        self.__played_movies.append(movie)

    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.actor_colleague

    def get_number_of_colleagues(self):
        return len(self.__actor_colleague)

    def __repr__(self):
        return "<Actor {}>".format(self.actor_full_name)

    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        if self.actor_full_name is None and other.actor_full_name is None:
            return False
        return self.actor_full_name == other.actor_full_name

    def __lt__(self, other):
        return self.actor_full_name < other.actor_full_name

    def __hash__(self):
        return hash(self.actor_full_name)


class Director:

    def __init__(self, director_full_name: str):
        self.__directed_movies = list()
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()

    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    @property
    def directed_movies(self):
        return iter(self.__directed_movies)

    def add_directed_movies(self, movie):
        self.__directed_movies.append(movie)

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        if not isinstance(other, Director):
            return False
        if self.director_full_name is None and other.director_full_name is None:
            return False
        return self.__director_full_name == other.director_full_name

    def __lt__(self, other):
        return self.__director_full_name < other.director_full_name

    def __hash__(self):
        return hash(self.__director_full_name)


class Genre:
    def __init__(self, genre_name: str):
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
            self.__classified_movies = None
        else:
            self.__genre_name = genre_name.strip()
            self.__classified_movies = list()


    @property
    def classified_movies(self):
        return iter(self.__classified_movies)

    @property
    def number_of_classified_movies(self):
        return len(self.__classified_movies)

    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def is_applied_to(self, movie):
        return movie in self.__classified_movies

    def add_Movie(self, movie):
        if isinstance(movie, Movie):
            if movie not in self.__classified_movies:
                self.__classified_movies.append(movie)

    def __repr__(self):
        return "<Genre {}>".format(self.__genre_name)

    def __eq__(self, other):
        if not isinstance(other, Genre):
            return False
        if self.genre_name is None and other.genre_name is None:
            return False
        return self.genre_name == other.genre_name

    def __lt__(self, other):
        return self.genre_name < other.genre_name

    def __hash__(self):
        return hash(self.genre_name)


class Movie:
    def __init__(self, title: str, release_year: int, id: int = None):
        self.__id = id
        self.__description = ""
        self.__director = None
        self.__actors = list()
        self.__genres = list()
        self.__reviews = list()
        self.__runtime_minutes = 0
        self.__revenue = 0
        # self.__cover_url = None

        if title != "" and type(title) is str and type(release_year) is int and release_year >= 1900:
            self.__title = title
            self.__release_year = release_year
        elif (title == "" or type(title) is not str) and (type(release_year) is int and release_year >= 1900):
            self.__title = None
            self.__release_year = release_year
        elif (type(release_year) is not int) and (len(title) > 0 and type(title) is str):
            self.__title = title
            self.__release_year = None
        else:
            self.__title = None
            self.__release_year = None
        # access = imdb.IMDb()
        # possible_movies = access.search_movie(self.__title)
        # self.__cover_url = possible_movies[0]['cover url']

    # @property
    # def cover_url(self) -> str:
    #     return self.__cover_url

    @property
    def revenue(self) -> float:
        return self.__revenue

    @property
    def title(self) -> str:
        return self.__title

    @property
    def id(self) -> int:
        return self.__id

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def description(self) -> str:
        return self.__description

    @property
    def director(self) -> Director:
        return self.__director

    @property
    def actors(self) -> list():
        return iter(self.__actors)

    @property
    def genres(self) -> list():
        return iter(self.__genres)

    @property
    def reviews(self) -> list():
        return iter(self.__reviews)

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @property
    def number_of_actors(self):
        return len(self.__actors)

    @property
    def number_of_reviews(self):
        return len(self.__reviews)

    @property
    def number_of_genres(self):
        return len(self.__genres)

    def set_description(self, new_description: str) -> bool:
        if type(new_description) is str:
            self.__description = new_description
            return True
        return False

    def set_director(self, new_director: Director) -> bool:
        if isinstance(new_director, Director):
            self.__director = new_director
            return True
        return False

    def set_runtime_minutes(self, new_runtime_minutes) -> bool:
        if type(new_runtime_minutes) is int:
            if new_runtime_minutes > 0:
                self.__runtime_minutes = new_runtime_minutes
                return True
            else:
                raise ValueError
        return False

    def set_revenue(self, revenue:float):
        if revenue >= 0:
            self.__revenue = revenue

    def add_actor(self, actor: Actor) -> bool:
        if isinstance(actor, Actor):
            self.__actors.append(actor)
            return True
        return False

    def remove_actor(self, actor: Actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre: Genre) -> bool:
        if isinstance(genre, Genre):
            if genre not in self.__genres:
                self.__genres.append(genre)
                return True
        return False

    def remove_genre(self, genre: Genre):
        if genre in self.__genres:
            self.__genres.remove(genre)

    def add_review(self, review):
        if isinstance(review, Review):
            self.__reviews.append(review)
            return True
        return False

    def is_classified_as(self, genre: Genre):
        return genre in self.__genres

    def __repr__(self):
        return "<Movie {}, {}>".format(self.title, self.release_year)

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return self.title == other.title and self.release_year == other.release_year

    def __lt__(self, other):
        if self.release_year == other.release_year:
            return self.title < other.title
        else:
            return self.release_year < other.release_year

    def __hash__(self):
        return hash((self.__title, self.__release_year))


class User:
    def __init__(self, user_name: str, password: str):
        self.__user_name = None
        self.__password = None
        if type(user_name) is str:
            if len(user_name) > 0:
                self.__user_name = user_name.lower()
        if type(password) is str:
            if len(password) > 0:
                self.__password = password
        self.__watched_movies = list()
        self.__reviews = list()
        self.__time_spent_watching_movies_minutes = 0

    @property
    def username(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies_minutes

    def __repr__(self):
        return "<User {}>".format(self.username)

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        if self.username is None and other.username is None:
            return False
        return self.username == other.username

    def __lt__(self, other):
        return self.username < other.username

    def __hash__(self):
        return hash((self.__user_name, self.__password))

    def watch_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            if movie not in self.__watched_movies:
                self.__watched_movies.append(movie)
                self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review):
        if isinstance(review, Review):
            if review not in self.__reviews:
                self.__reviews.append(review)


class Review:
    def __init__(self, user: User, movie: Movie, review_text: str, rating: int, timestamp: datetime):
        self.__author = user
        self.__movie = movie
        self.__review_text = review_text
        self.__rating = None
        self.__timestamp = timestamp
        if type(rating) is int:
            if 0 < rating <= 10:
                self.__rating = rating

    @property
    def review_author(self) -> User:
        return self.__author

    @property
    def movie(self) -> Movie:
        return self.__movie

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return "<Review {}, {}>".format(self.movie, self.timestamp)

    def __eq__(self, other):
        if self.movie == other.movie and self.review_text == other.review_text \
                and self.rating == other.rating and self.timestamp == other.timestamp:
            return True
        return False

    def hash(self):
        return hash((self.movie, self.timestamp))


class WatchList:
    def __init__(self):
        self.__watchlist = list()
        self.__start_index = 0
        self.__schedule = dict();

    @property
    def watchlist(self):
        return self.__watchlist

    def add_movie(self, movie: Movie, date: datetime):
        if isinstance(movie, Movie):
            if movie not in self.__watchlist:
                self.__watchlist.append(movie)
                self.__schedule[movie] = date

    def remove_movie(self, movie: Movie):
        try:
            self.__watchlist.remove(movie)
            del self.__schedule[movie]
        except ValueError:
            return False

    def get_schedule(self):
        return self.__schedule

    def print_schedule(self):

        output_str = "You have scheduled the following movies to watch in the future: \n"
        sorted_schedule = sorted(self.__schedule.items(), key=lambda current: current[1], reverse=False)
        for movie in sorted_schedule:
            output_str += "Movie: " + str(movie[0].title) + ", " + str(
                movie[0].release_year) + " is schedule on " + str(movie[1].day) + "/" + \
                          str(movie[1].month) + "/" + str(movie[1].year) + "\n"
        return output_str

    def select_movie_to_watch(self, index: int):
        if index < 0:
            return None
        try:
            return self.__watchlist[index]
        except IndexError:
            return None

    def size(self):
        return len(self.__watchlist)

    def first_movie_in_watchlist(self):
        movie = None
        if self.size() > 0:
            movie = self.__watchlist[0]
        return movie

    def __iter__(self):
        return iter(self.__watchlist)

    def __next__(self):
        try:
            to_return = self.self.__watchlist[self.__start_index]
            self.__start_index += 1
            return to_return
        except IndexError:
            raise StopIteration


class ModelException(Exception):
    pass


def add_movie_attributes(movie: Movie, list_of_genres: List[Genre],
                         description: str, list_of_actors: List[Actor],
                         director: Director, runtime: int):

    # Add actors to movie and construct actor colleagues
    for actor in list_of_actors:
        for colleague in list_of_actors:
            if colleague is not actor:
                actor.add_actor_colleague(colleague)

    # Add director to movie
    # movie.set_director(director)

    # Set movie description
    movie.set_description(description)

    # Set movie runtime
    movie.set_runtime_minutes(runtime)


def make_review(review_text: str, user: User, movie: Movie, rating: int, timestamp: datetime = datetime.today()):
    review = Review(user=user, movie=movie, review_text=review_text, rating=rating, timestamp=timestamp)
    user.add_review(review)
    movie.add_review(review)

    return review
