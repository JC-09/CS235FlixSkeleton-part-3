from datetime import date
import pytest

from CS235Flix.authentication.services import AuthenticationException
from CS235Flix.movies import services as movies_services
from CS235Flix.authentication import services as auth_services
from CS235Flix.movies.services import NonExistentMovieException, NonExistentActorException, NonExistentDirectorException, NoSearchResultsException


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)

def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_id = 2
    review_text = 'What a great movie!'
    username = 'fmercury'
    rating = 10

    # Call the service layer to add the review
    movies_services.add_review(review_text=review_text, username=username,
                               movie_id=movie_id, rating=rating, repo=in_memory_repo)

    # Retrieve the reviews for the movie from the repository
    reviews_as_dict = movies_services.get_reviews_for_movie(movie_id=movie_id, repo=in_memory_repo)

    # Check that the reviews include a review with the new review text
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text), None
    ) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 20
    review_text = 'What a great movie!'
    username = 'fmercury'
    rating = 10

    # Call the service layer to attempt add the review
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.add_review(review_text=review_text, username=username,
                                   movie_id=movie_id, rating=rating, repo=in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_id = 2
    review_text = 'What a great movie!'
    username = 'unknownUser'
    rating = 10

    # Call the service layer to attempt add the review
    with pytest.raises(movies_services.UnknownUserException):
        movies_services.add_review(review_text=review_text, username=username,
                                   movie_id=movie_id, rating=rating, repo=in_memory_repo)


def test_can_get_a_movie(in_memory_repo):
    movie_id = 1
    movie_as_dict = movies_services.get_movie(movie_id=movie_id, repo=in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['title'] == 'Guardians of the Galaxy'
    assert movie_as_dict['release_year'] == 2014
    assert movie_as_dict['description'] == 'A group of intergalactic criminals are forced to work together to stop a fanatical warrior from taking control of the universe.'
    assert movie_as_dict['director'] == 'James Gunn'
    assert movie_as_dict['runtime_minutes'] == 121

    actor_fullnames = [dictionary['actor_fullname'] for dictionary in movie_as_dict['actors']]
    assert 'Chris Pratt' in actor_fullnames
    assert 'Vin Diesel' in actor_fullnames
    assert 'Bradley Cooper' in actor_fullnames
    assert 'Zoe Saldana' in actor_fullnames

    genres = [dictionary['genre_name'] for dictionary in movie_as_dict['genres']]
    assert 'Action' in genres
    assert 'Adventure' in genres
    assert 'Sci-Fi' in genres


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 33

    # Call the service layer to attempt to retrieve the Movie
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movie(movie_id, in_memory_repo)


def test_get_latest_movie(in_memory_repo):
    movie_as_dict = movies_services.get_latest_movie(in_memory_repo)

    assert movie_as_dict['id'] == 7


def test_get_oldest_movie(in_memory_repo):
    movie_as_dict = movies_services.get_oldest_movie(in_memory_repo)

    assert movie_as_dict['id'] == 2


def test_get_movies_by_release_year_with_one_movie_in_the_year(in_memory_repo):
    target_year = 2012

    movies_as_dict, prev_year, next_year = movies_services.get_movies_by_release_year(target_year, in_memory_repo)
    assert len(movies_as_dict) == 1
    assert movies_as_dict[0]['id'] == 2

    assert prev_year is None
    assert next_year == 2014


def test_get_movies_by_release_year_with_multiple_movies_in_the_year(in_memory_repo):
    target_year = 2016

    movies_as_dict, prev_year, next_year = movies_services.get_movies_by_release_year(target_year, in_memory_repo)

    # Check that there are 8 movies released in 2016 in the repository
    assert len(movies_as_dict) == 8

    # Check that the movie ids for the movies returned are 3, 4, 5, 6, 7, 8, 9, 10
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([3, 4, 5, 6, 7, 8, 9, 10]).issubset(movie_ids)

    # Check that the dates of movies surrounding the target year are 2014 and None
    assert prev_year == 2014
    assert next_year is None


def test_get_movies_by_release_year_with_non_existent_release_year(in_memory_repo):

    target_year = 2010

    movies_as_dict, prev_year, next_year = movies_services.get_movies_by_release_year(target_year, in_memory_repo)

    assert len(movies_as_dict) == 0


def test_get_movies_by_id(in_memory_repo):
    target_movie_ids = [3, 6, 17, 19]
    movies_as_dict = movies_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    # Check that 2 movies were returned from the query
    assert len(movies_as_dict) == 2

    # Check that the movie ids returned were 3 and 6
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([3,6]).issubset(movie_ids)


def test_search_movies_by_actor_fullname(in_memory_repo):
    target_actor = "Chris Pratt"
    movies_as_dict = movies_services.search_movie_by_actor_fullname(target_actor, in_memory_repo)

    # Check that 2 movies were returned from the query
    assert len(movies_as_dict) == 2

    # Check that the movie ids returned were 1 and 10
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert 1 in movie_ids
    assert 10 in movie_ids


def test_search_movies_by_non_existent_actor(in_memory_repo):
    non_existent_actor = 'Not Exist'
    with pytest.raises(NonExistentActorException):
        movies_as_dict = movies_services.search_movie_by_actor_fullname(non_existent_actor, in_memory_repo)


def test_search_movies_by_director_fullname(in_memory_repo):
    target_director = "M. Night Shyamalan"
    movies_as_dict = movies_services.search_movie_directed_by_director_fullname(target_director, in_memory_repo)

    # Check that 1 movie is returned from the query
    assert len(movies_as_dict) == 1

    # Check that the movie id is 3
    assert movies_as_dict[0]['id'] == 3


def test_search_movies_by_non_existent_director_fullname(in_memory_repo):
    non_existent_director = 'Not Exist'
    with pytest.raises(NonExistentDirectorException):
        movies_as_dict = movies_services.search_movie_directed_by_director_fullname(non_existent_director, in_memory_repo)


def test_search_by_a_valid_actor_name_and_a_valid_director_name(in_memory_repo):
    target_actor = 'Ryan Gosling'
    target_director = 'Damien Chazelle'
    movies_as_dict = movies_services.search_movie_by_actor_and_director(target_actor, target_director, in_memory_repo)

    # Check that 1 movie is returned from the query
    assert len(movies_as_dict) == 1

    # Check that the movie id is 7
    assert movies_as_dict[0]['id'] == 7


def test_search_an_invalid_actor_name_or_an_invalid_director_name(in_memory_repo):
    correct_actor = 'Ryan Gosling'
    correct_director = 'Damien Chazelle'
    fake_actor = 'Fake Actor'
    fake_director = 'Fake Director'

    with pytest.raises(NoSearchResultsException):
        # Check that no movie is returned for the combination of correct actor and fake director
        movies_as_dict = movies_services.search_movie_by_actor_and_director(correct_actor, fake_director, in_memory_repo)
        assert len(movies_as_dict) == 0

        # Check that no movie is returned for the combination of fake actor and correct director
        movies_as_dict = movies_services.search_movie_by_actor_and_director(fake_actor, correct_director, in_memory_repo)
        assert len(movies_as_dict) == 0

        # Check that no movie is returned for the combination of fake actor and fake director
        movies_as_dict = movies_services.search_movie_by_actor_and_director(fake_actor, fake_director, in_memory_repo)
        assert len(movies_as_dict) == 0


def test_search_a_valid_movie_title(in_memory_repo):
    movies_as_dict = movies_services.search_movie_by_title('La La Land', in_memory_repo)
    assert movies_as_dict[0]['id'] == 7


def test_search_a_non_existent_movie_title(in_memory_repo):

    with pytest.raises(NoSearchResultsException):
        movies_as_dict = movies_services.search_movie_by_title('3sdf4as5df14as35d1few', in_memory_repo)
        assert len(movies_as_dict) == 0


def test_get_reviews_for_movie(in_memory_repo):
    reviews_as_dict = movies_services.get_reviews_for_movie(1, in_memory_repo)

    # Check that 3 reviews were returned for movie with id 1
    assert len(reviews_as_dict) == 3

    # Check that the reviews relate to the movie whose id is 1
    movie_ids = [review['movie_id'] for review in reviews_as_dict]
    movie_ids = set(movie_ids)
    assert 1 in movie_ids and len(movie_ids) == 1


def test_get_reviews_for_non_existent_movies(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        reviews_as_dict = movies_services.get_reviews_for_movie(30, in_memory_repo)


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    reviews_as_dict = movies_services.get_reviews_for_movie(8, in_memory_repo)
    assert len(reviews_as_dict) == 0


def test_get_top_5_movies_by_revenue(in_memory_repo):
    movies = movies_services.get_top_6_movies_by_revenue(in_memory_repo)
    assert len(movies) == 6

    assert movies[0]['title'] == "Guardians of the Galaxy"
    assert movies[1]['title'] == "Suicide Squad"
    assert movies[2]['title'] == "Sing"
    assert movies[3]['title'] == "La La Land"
    assert movies[4]['title'] == "Split"
    assert movies[5]['title'] == "Prometheus"


def test_get_suggestions_for_a_user(in_memory_repo):
    username = "thorke"
    suggestions = movies_services.get_suggestions_for_a_user(username=username, repo=in_memory_repo)
    assert len(suggestions) == 1
    assert suggestions[0]['title'] == "Guardians of the Galaxy"







