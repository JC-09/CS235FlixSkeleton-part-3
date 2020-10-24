from datetime import date, datetime

import pytest

from CS235Flix.adapters.database_repository import SqlAlchemyRepository
from CS235Flix.domainmodel.model import User, Genre, Actor, Director, Movie, Review, make_review
from CS235Flix.adapters.repository import RepositoryException


def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = User('Dave', '123456789')
    print(user)
    repo.add_user(user)

    repo.add_user(User('Martin', '123456789'))

    user2 = repo.get_user('Dave')
    print(user2)
    assert user2 == user and user2 is user


def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('fmercury')
    assert user == User('fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None


def test_repository_can_add_an_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    actor = Actor("Keanu Reeves")
    repo.add_actor(actor)

    assert repo.get_actor("Keanu Reeves") == actor and repo.get_actor("Keanu Reeves") is actor


def test_repository_can_retrieve_an_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    actor = repo.get_actor("Chris Pratt")
    assert actor == Actor("Chris Pratt")
    assert Movie("Guardians of the Galaxy", 2014) in actor.played_movies


def test_repository_returns_none_for_non_existent_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    actor = repo.get_actor('Fake Actor')
    assert actor is None


def test_repository_can_check_existence_of_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.check_actor_existence_in_repo(Actor("Fake Actor")) is False
    assert repo.check_actor_existence_in_repo(Actor("Matt Damon")) is True


def test_repository_can_retrieve_correct_actor_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_total_number_of_actors() == 39


def test_repository_can_add_a_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    director = Director("Chad Stahelski")
    repo.add_director(director)
    assert repo.get_director("Chad Stahelski") == director and repo.get_director("Chad Stahelski") is director


def test_repository_can_retrieve_a_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    director = repo.get_director('Sean Foley')
    assert director == Director('Sean Foley')
    assert Movie('Mindhorn', 2016) in director.directed_movies


def test_repository_returns_none_for_non_existent_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_director("Fake Director") is None


def test_repository_can_retrieve_correct_director_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_total_number_of_directors() == 10


def test_repository_can_add_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre = Genre('Some New Genre')
    repo.add_genre(genre)
    assert repo.get_genre('Some New Genre') == genre and repo.get_genre('Some New Genre') is genre


def test_repository_can_retrieve_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genre = repo.get_genre('Sci-Fi')
    assert genre == Genre('Sci-Fi')
    assert Movie("Guardians of the Galaxy", 2014) in genre.classified_movies


def test_repository_can_retrieve_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    genres = repo.get_genres()
    assert len(genres) == 14

    genre_one = [genre for genre in genres if genre.genre_name == 'Sci-Fi'][0]  # Should have 2 matches
    genre_two = [genre for genre in genres if genre.genre_name == 'Comedy'][0]  # Should have 3 matches

    assert genre_one.number_of_classified_movies == 2
    assert genre_two.number_of_classified_movies == 3


def test_repository_can_retrieve_correct_genre_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_total_number_of_genres_in_repo() == 14


def test_repository_can_check_existence_of_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.check_genre_existence(Genre("Fake Genre")) is False
    assert repo.check_genre_existence(Genre("Animation")) is True
    assert repo.check_genre_existence(Genre("Family")) is True


def test_repository_can_add_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = Movie('Avengers : End Game', 2019)
    repo.add_movie(movie)

    assert repo.get_movie("Avengers : End Game", 2019) == movie and repo.get_movie("Avengers : End Game", 2019) is movie


def test_repository_can_retrieve_movie_by_title_and_release_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movie = repo.get_movie("Guardians of the Galaxy", 2014)

    # Check that the movie has expected attributes
    assert movie.description == "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."
    assert movie.director == Director("James Gunn")
    assert movie.runtime_minutes == 121
    actors = iter(movie.actors)
    assert next(actors) == Actor("Chris Pratt")
    assert next(actors) == Actor("Vin Diesel")
    assert next(actors) == Actor("Bradley Cooper")
    assert next(actors) == Actor("Zoe Saldana")

    # Check that the movie has the expected genre(s)
    assert movie.is_classified_as(Genre("Action"))
    assert movie.is_classified_as(Genre("Adventure"))
    assert movie.is_classified_as(Genre("Sci-Fi"))

    # Check that the movie has the correct reviews
    assert movie.number_of_reviews == 3

    review_1 = [review for review in movie.reviews if review.review_text == "This movie is great!"][0]
    review_2 = [review for review in movie.reviews if review.review_text == "This movie is awesome"][0]
    assert review_1.review_author.username == "fmercury"
    assert review_2.review_author.username == "thorke"


def test_repository_can_retrieve_movies_by_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies_2014 = repo.get_movies_by_release_year(2014)

    movies_2016 = repo.get_movies_by_release_year(2016)
    assert len(movies_2014) == 1
    assert len(movies_2016) == 8


def test_repository_does_not_retrieve_movie_when_there_are_no_movies_for_a_given_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    movies_1800 = repo.get_movies_by_release_year(1800)
    movies_2030 = repo.get_movies_by_release_year(2030)
    assert len(movies_1800) == 0
    assert len(movies_2030) == 0


def test_repository_can_retrieve_a_list_of_movies_by_an_actor_fullname(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_of_movies_played_by_Bradley_Cooper = repo.get_movies_played_by_an_actor("Bradley Cooper")
    assert len(list_of_movies_played_by_Bradley_Cooper) == 1
    assert list_of_movies_played_by_Bradley_Cooper[0].title == "Guardians of the Galaxy"

    list_of_movies_played_by_Chris_Pratt = repo.get_movies_played_by_an_actor("Chris Pratt")
    assert len(list_of_movies_played_by_Chris_Pratt) == 2
    assert list_of_movies_played_by_Chris_Pratt[0].title == "Guardians of the Galaxy"
    assert list_of_movies_played_by_Chris_Pratt[1].title == "Passengers"

    list_of_movies_played_by_Chris_Pratt = repo.get_movies_played_by_an_actor("   chris PRATT   ")
    assert len(list_of_movies_played_by_Chris_Pratt) == 2
    assert list_of_movies_played_by_Chris_Pratt[0].title == "Guardians of the Galaxy"
    assert list_of_movies_played_by_Chris_Pratt[1].title == "Passengers"


def test_repository_returns_an_empty_list_of_movie_for_non_existent_actor(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_of_movies_played_by_fake_actor = repo.get_movies_played_by_an_actor('Fake Actor')

    assert len(list_of_movies_played_by_fake_actor) == 0


def test_repository_returns_a_list_of_movies_directed_by_a_valid_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_of_movies_directed_by_James_Gunn = repo.get_movies_directed_by_a_director("James Gunn")
    assert len(list_of_movies_directed_by_James_Gunn) == 1
    assert list_of_movies_directed_by_James_Gunn[0].title == "Guardians of the Galaxy"


def test_repository_returns_empty_list_of_movie_for_non_existent_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_of_movies = repo.get_movies_directed_by_a_director('Fake Director')
    assert len(list_of_movies) == 0


def test_repository_can_retrieve_the_top_6_highest_revenue_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = repo.get_top_6_highest_revenue_movies()
    print(movies)
    assert len(movies) == 6

    assert movies[0].title == "Guardians of the Galaxy"
    assert movies[1].title == "Suicide Squad"
    assert movies[2].title == "Sing"
    assert movies[3].title == "La La Land"
    assert movies[4].title == "Split"
    assert movies[5].title == "Prometheus"


def test_repository_returns_a_list_of_movies_based_on_actor_and_director(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_of_movies = repo.search_movies_by_actor_and_director('Ryan Gosling', 'Damien Chazelle')
    assert len(list_of_movies) == 1
    assert list_of_movies[0].title == 'La La Land'


def test_repository_returns_an_empty_list_for_invalid_actor_name_or_director_name(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    invalid_actor = repo.search_movies_by_actor_and_director('Fake Actor', 'Damien Chazelle')
    assert len(invalid_actor) == 0

    invalid_director = repo.search_movies_by_actor_and_director('Ryan Gosling', 'Fake Director')
    assert len(invalid_director) == 0

    both_invalid = repo.search_movies_by_actor_and_director('Fake Actor', 'Fake Director')
    assert len(both_invalid) == 0


def test_repository_returns_a_list_of_movies_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    # test search by exact title
    list_of_movies = repo.search_movie_by_title('Suicide Squad')
    assert len(list_of_movies) == 1
    assert list_of_movies[0].id == 5

    # test search by fuzzy title
    list_of_movies = repo.search_movie_by_title("the")
    assert len(list_of_movies) == 4

    list_of_movies_titles = [movie.title for movie in list_of_movies]
    assert "Prometheus" in list_of_movies_titles
    assert "Guardians of the Galaxy" in list_of_movies_titles
    assert "The Great Wall" in list_of_movies_titles
    assert "The Lost City of Z" in list_of_movies_titles


def test_repository_can_get_the_latest_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_latest_movie()
    assert movie.title == 'Split'
    assert movie.release_year == 2016


def test_repository_can_get_the_oldest_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_oldest_movie()
    assert movie.release_year == 2012
    assert movie.title == "Prometheus"


def test_repository_returns_release_year_of_previous_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie_by_index(1)
    previous_year = repo.get_release_year_of_previous_movie(movie)

    assert previous_year == 2012  # 2013 for 1000 movies


def test_repository_returns_none_when_there_are_no_previous_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie_by_index(2)
    previous_year = repo.get_release_year_of_previous_movie(movie)

    assert previous_year is None


def test_repository_returns_release_year_of_next_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie_by_index(1)
    next_year = repo.get_release_year_of_next_movie(movie)
    assert next_year == 2016 # 2015 if using the full 1000 movies


def test_repository_returns_none_when_there_are_no_next_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie_by_index(3)
    next_year = repo.get_release_year_of_next_movie(movie)
    assert next_year is None


def test_repository_can_retrieve_correct_movie_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    number_of_movies = repo.get_total_number_of_movies_in_repo()
    assert number_of_movies == 10


def test_repository_can_retrieve_movie_by_index(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie_by_index(1)

    # Check that the movie has expected attributes
    assert movie.title == "Guardians of the Galaxy"
    assert movie.release_year == 2014
    assert movie.description == "A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe."
    assert movie.director == Director("James Gunn")
    assert movie.runtime_minutes == 121
    actors = iter(movie.actors)
    assert next(actors) == Actor("Chris Pratt")
    assert next(actors) == Actor("Vin Diesel")
    assert next(actors) == Actor("Bradley Cooper")
    assert next(actors) == Actor("Zoe Saldana")

    # Check that the movie has the expected genre(s)
    assert movie.is_classified_as(Genre("Action"))
    assert movie.is_classified_as(Genre("Adventure"))
    assert movie.is_classified_as(Genre("Sci-Fi"))

    # Check that the movie has the correct reviews
    assert movie.number_of_reviews == 3

    review_1 = [review for review in movie.reviews if review.review_text == "This movie is great!"][0]
    review_2 = [review for review in movie.reviews if review.review_text == "This movie is awesome"][0]
    assert review_1.review_author.username == "fmercury"
    assert review_2.review_author.username == "thorke"


def test_repository_can_retrieve_a_list_of_movie_indexes_by_a_genre_name(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_of_movie_indexes_for_Sci_Fi = repo.get_movie_indexes_for_genre("Sci-Fi")
    list_of_movie_indexes_for_Horror = repo.get_movie_indexes_for_genre("Horror")

    assert len(list_of_movie_indexes_for_Sci_Fi) == 2
    assert len(list_of_movie_indexes_for_Horror) == 1


def test_repository_returns_an_empty_list_of_movie_indexes_for_non_existent_genre_name(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_of_movie_indexes_for_Fake_Genre = repo.get_movie_indexes_for_genre("Fake Genre")
    assert len(list_of_movie_indexes_for_Fake_Genre) == 0


def test_repository_can_get_a_list_of_actors_of_a_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie_by_index(1)
    list_of_actors = list(repo.get_movie_actors(movie))

    assert Actor('Chris Pratt') in list_of_actors
    assert Actor('Vin Diesel') in list_of_actors
    assert Actor('Bradley Cooper') in list_of_actors
    assert Actor('Zoe Saldana') in list_of_actors
    assert Actor('Fake Actor') not in list_of_actors


def test_repository_can_get_the_release_year_of_a_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie_by_index(10)
    assert 2016 == repo.get_movie_release_year(movie)


def test_repository_can_get_reviews_from_a_movie(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie_reviews = iter(repo.get_movie_reviews(repo.get_movie_by_index(1)))

    assert next(movie_reviews).review_text == "This movie is great!"
    assert next(movie_reviews).review_text == "This movie is awesome"
    assert next(movie_reviews).review_text == "Love it!"
    with pytest.raises(StopIteration):
        assert repr(next(movie_reviews).review_text) == StopIteration


def test_repository_can_get_expected_movie_genres(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie_genres = iter(repo.get_movie_genres(repo.get_movie_by_index(10)))
    assert next(movie_genres) == Genre("Adventure")
    assert next(movie_genres) == Genre("Drama")
    assert next(movie_genres) == Genre("Romance")
    with pytest.raises(StopIteration):
        assert repr(next(movie_genres)) == StopIteration


def test_repository_can_retrieve_movies_for_a_indexes_list(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = repo.get_movies_by_index([1, 3, 7, 10])

    assert movies[0].title == 'Guardians of the Galaxy'
    assert movies[1].title == 'Split'
    assert movies[2].title == 'La La Land'
    assert movies[3].title == 'Passengers'


def test_repository_does_not_retrieve_movies_for_non_existent_indexes(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = repo.get_movies_by_index([2, 35455647])

    assert len(movies) == 1
    assert movies[0].title == "Prometheus"


def test_repository_returns_an_empty_list_for_non_existent_indexes(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = repo.get_movies_by_index([22222, 33333])
    assert len(movies) == 0


def test_repository_does_not_add_a_review_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movie = repo.get_movie_by_index(3)
    review = Review(user=None, movie=movie, review_text="testing", rating=6, timestamp=date.today())
    with pytest.raises(RepositoryException):
        repo.add_review(review)


def test_repository_does_not_add_a_review_without_a_movie_properly_attached(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('thorke')
    movie = repo.get_movie_by_index(1)
    review = Review(user=user,
                    movie=None,
                    review_text="Awesome!",
                    rating=10,
                    timestamp=date.today())

    with pytest.raises(RepositoryException):
        # Exception expected because the Review doesn't refer to the Movie
        repo.add_review(review)


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = repo.get_user('thorke')
    movie = repo.get_movie_by_index(10)
    review = Review(user=user,
                    movie=movie,
                    review_text='Great!',
                    rating=10,
                    timestamp=date.today())
    assert repo.get_total_number_of_reviews() == 4
    assert review in repo.get_movie_reviews(movie)
    assert review in repo.get_user_reviews(user)


def test_repository_retrieves_all_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_of_reviews = repo.get_reviews()

    assert len(list_of_reviews) == 3


def test_repository_can_retrieve_a_list_of_movies_reviewed_by_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    movies = repo.get_user_reviewed_movie("thorke")
    assert len(movies) == 1
    assert movies[0].id == 1


def test_repository_can_get_a_list_of_genres_based_on_a_users_reviewed_movies(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    guardian_of_the_galaxy = repo.get_movie_by_index(1)
    reviewed_movies = [guardian_of_the_galaxy]
    genre_list = repo.get_user_interested_genre_from_reviewed_movies(reviewed_movies)

    assert len(genre_list) == 3
    assert genre_list[0].genre_name == "Action"
    assert genre_list[1].genre_name == "Adventure"
    assert genre_list[2].genre_name == "Sci-Fi"


def test_repository_can_retrieve_the_top_movie_classified_by_a_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    list_of_genres = repo.get_genres()
    action = [genre for genre in list_of_genres if genre.genre_name == "Action"]
    action = action[0]
    top_action = repo.get_top_movie_by_genre(action)
    assert top_action.title == "Guardians of the Galaxy"

    fantasy = [genre for genre in list_of_genres if genre.genre_name == "Fantasy"]
    fantasy = fantasy[0]
    top_fantasy = repo.get_top_movie_by_genre(fantasy)
    assert top_fantasy.title == "Suicide Squad"


def test_repository_can_suggest_desired_movies_to_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    username = "thorke"
    suggestions = repo.get_suggestion_for_user(username=username)

    assert len(suggestions) == 1
    assert repo.get_movie_by_index(1) in suggestions


def test_earliest_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_earliest_year() == 2012


def test_latest_year(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    assert repo.get_latest_year() == 2016