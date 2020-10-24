from CS235Flix.domainmodel.model import Genre


class TestGenreMethods:
    def test_init(self):
        genre1 = Genre("Horror")
        assert repr(genre1) == "<Genre Horror>"
        genre2 = Genre("")
        assert genre2.genre_name is None

    def test_eq(self):
        genre1 = Genre("Horror")
        genre2 = Genre("")
        genre3 = Genre("Horror")
        genre4 = Genre(1)
        assert genre1.__eq__(genre2) == False
        assert genre1.__eq__(genre3) == True
        assert genre2.__eq__(genre4) == False


    def test_lt(self):
        genre1 = Genre("Horror")
        genre2 = Genre("Romantic")
        assert genre1.__lt__(genre2) == True

    def test_hash(self):
        genre1 = Genre("Horror")
        assert hash(genre1) == hash("Horror")