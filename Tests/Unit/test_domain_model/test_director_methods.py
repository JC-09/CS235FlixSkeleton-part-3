from CS235Flix.domainmodel.model import Director


class TestDirectorMethods:

    def test_init(self):
        director1 = Director("Taika Waititi")
        assert repr(director1) == "<Director Taika Waititi>"
        director2 = Director("")
        assert director2.director_full_name is None
        director3 = Director(42)
        assert director3.director_full_name is None

    def test_equal(self):
        director1 = Director("Taika Waititi")
        director2 = Director("Some Director")
        assert director1.__eq__(director2) == False
        assert director2.__eq__(director1) == False
        director3 = Director(1)
        assert director2.__eq__(director3) == False
        director4 = Director("Taika Waititi")
        assert director1.__eq__(director4) == True

    def test_lt(self):
        director1 = Director("Taika Waititi")
        director2 = Director("Some Director")
        assert director2.__lt__(director1) == True

    def test_hash(self):
        director1 = Director("Taika Waititi")
        assert director1.__hash__() == hash("Taika Waititi")
