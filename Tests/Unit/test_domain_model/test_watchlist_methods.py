from CS235Flix.domainmodel.model import User, Movie, WatchList
from datetime import datetime
import pytest

@pytest.fixture
def watchlist():
    return WatchList()

def test_init(watchlist):
    assert watchlist.size() == 0

def test_size_after_adding_movies(watchlist):
    watchlist.add_movie(Movie("Moana", 2016, 1), datetime(2020, 9, 3))
    watchlist.add_movie(Movie("Ice Age", 2002, 2), datetime(2020, 9, 1))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012, 3), datetime(2020, 9, 15))
    assert watchlist.size() == 3
    assert len(watchlist.get_schedule()) == 3

def test_add_movie(watchlist):
    watchlist.add_movie(Movie("Moana", 2016, 1), datetime(2020, 9, 3))
    watchlist.add_movie(Movie("Ice Age", 2002, 2), datetime(2020, 9, 1))
    assert watchlist.size() == 2
    assert len(watchlist.get_schedule())== 2
    watchlist.add_movie(Movie("Ice Age", 2002, 2), datetime(2020, 9, 1))
    assert watchlist.size() == 2
    assert len(watchlist.get_schedule()) == 2
    watchlist.add_movie(User("username", "password"), datetime(2020,9,4)) #test if the function handles none Movie type object
    assert watchlist.size() == 2
    assert len(watchlist.get_schedule()) == 2

def test_remove_movie(watchlist):
    watchlist.add_movie(Movie("Moana", 2016, 1), datetime(2020, 9, 3))
    watchlist.add_movie(Movie("Ice Age", 2002, 2), datetime(2020, 9, 1))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012, 3), datetime(2020, 9, 15))
    watchlist.remove_movie(Movie("Ice Age", 2002, 2))
    assert watchlist.size() == 2
    assert len(watchlist.get_schedule()) == 2
    watchlist.remove_movie(Movie("Star War", 2017, 4))  #remove an movie that doesn't exist in the watchlist
    assert watchlist.size() == 2
    assert len(watchlist.get_schedule()) == 2

def test_select_movie_to_watch(watchlist):
    watchlist.add_movie(Movie("Moana", 2016, 1), datetime(2020, 9, 3))
    watchlist.add_movie(Movie("Ice Age", 2002, 2), datetime(2020, 9, 1))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012, 3), datetime(2020, 9, 15))
    assert repr(watchlist.select_movie_to_watch(0)) == "<Movie Moana, 2016>"
    assert watchlist.select_movie_to_watch(-1) is None
    assert watchlist.select_movie_to_watch(3) is None

def test_first_movie_in_watchlist(watchlist):
    assert watchlist.first_movie_in_watchlist() is None
    watchlist.add_movie(Movie("Moana", 2016, 1), datetime(2020, 9, 3))
    watchlist.add_movie(Movie("Ice Age", 2002, 2), datetime(2020, 9, 1))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012, 3), datetime(2020, 9, 15))
    assert repr(watchlist.first_movie_in_watchlist()) == "<Movie Moana, 2016>"

def test_iter_and_next(watchlist):
    watchlist.add_movie(Movie("Moana", 2016, 1), datetime(2020, 9, 3))
    watchlist.add_movie(Movie("Ice Age", 2002, 2), datetime(2020, 9, 1))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012, 3), datetime(2020, 9, 15))
    i = iter(watchlist)
    assert repr(next(i)) == "<Movie Moana, 2016>"
    assert repr(next(i)) == "<Movie Ice Age, 2002>"
    assert repr(next(i)) == "<Movie Guardians of the Galaxy, 2012>"
    with pytest.raises(StopIteration):
        assert repr(next(i)) == StopIteration

def test_print_schedule(watchlist):
    watchlist.add_movie(Movie("Moana", 2016, 1), datetime(2020, 9, 3))
    watchlist.add_movie(Movie("Ice Age", 2002, 2), datetime(2020, 9, 1))
    watchlist.add_movie(Movie("Guardians of the Galaxy", 2012, 3), datetime(2020, 9, 15))
    assert watchlist.print_schedule() == "You have scheduled the following movies to watch in the future: \nMovie: Ice Age, 2002 is schedule on 1/9/2020\nMovie: Moana, " \
         "2016 is schedule on 3/9/2020\nMovie: Guardians of the Galaxy, 2012 is schedule on 15/9/2020\n"

