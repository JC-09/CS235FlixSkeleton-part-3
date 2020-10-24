from CS235Flix.domainmodel.model import Movie, Review, User
from datetime import date

class TestReviewMethods:
    def test_init(self):
        user = User("username", "password")
        movie = Movie("Moana", 2016, 1)
        review_text = "This movie was very enjoyable."
        rating = 8
        review = Review(user, movie, review_text, rating, date.fromisoformat('2020-03-15'))
        assert review.review_author == user
        assert repr(review.movie) == "<Movie Moana, 2016>"
        assert review.review_text == "This movie was very enjoyable."
        assert review.rating == 8