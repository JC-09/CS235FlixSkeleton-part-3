from CS235Flix.domainmodel.model import Movie, Actor, Director
import pytest
class TestMovieMethods:
    def test_init(self):
        movie1 = Movie("Moana", 2016, 4)
        assert repr(movie1) == "<Movie Moana, 2016>"

    def test_director(self):
        movie1 = Movie("Moana", 2016, 1)
        movie1.set_director(Director("Ron Clements"))
        assert repr(movie1.director) == "<Director Ron Clements>"

    def test_add_actors(self):
        movie1 = Movie("Moana", 2016, 3)

        actors = [Actor("Auli'i Cravalho"), Actor("Dwayne Johnson"), Actor("Rachel House"), Actor("Temuera Morrison")]
        i = iter(movie1.actors)
        for actor in actors:
            movie1.add_actor(actor)
            next(i) == actor

    def test_movie_runtime_minutes(self):
        movie1 = Movie("Moana", 2016, 1)
        movie1.set_runtime_minutes(107)
        assert movie1.runtime_minutes == 107

        with pytest.raises(ValueError):
            movie1 = Movie("Kong", 2016, 3)
            movie1.set_runtime_minutes(-6)
            assert movie1.runtime_minutes == ValueError

    def test_remove_actor(self):
        movie1 = Movie("Moana", 2016, 2)
        movie1.add_actor(Actor("Some Actor"))
        assert movie1.number_of_actors == 1
        movie1.remove_actor(Actor("Some Actor"))
        assert movie1.number_of_actors == 0
        movie1.remove_actor(Actor("Some Actor"))

    def test_hash_function(self):
        movie1 = Movie("Moana", 2016, 1)
        assert movie1.__hash__() == hash(("Moana", 2016))

    def test_lt(self):
        movie1 = Movie("Moana", 2016, 1)
        movie2 = Movie("Apple", 2019, 2)
        movie3 = Movie("Apple", 2020, 3)
        movie4 = Movie("Apple", 2016, 4)
        assert movie1.__lt__(movie2) == True
        assert movie2.__lt__(movie1) == False
        assert movie2.__lt__(movie3) == True
        assert movie4.__lt__(movie1) == True

    def test_release_year(self):
        movie1 = Movie("Moana", 2016, 1)
        movie2 = Movie("Apple", "abc", 3)
        movie3 = Movie("Wrong", 1800, 2)
        assert movie1.release_year == 2016
        assert movie2.release_year is None
        assert movie3.release_year is None