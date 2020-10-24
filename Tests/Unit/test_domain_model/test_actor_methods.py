from CS235Flix.domainmodel.model import Actor


class TestActorMethods:
    def test_init(self):
        actor1 = Actor("Angelina Jolie")
        actor2 = Actor("")
        assert repr(actor1) == "<Actor Angelina Jolie>"
        assert actor2.actor_full_name is None

    def test_equal(self):
        actor1 = Actor("Angelina Jolie")
        actor2 = Actor("")
        actor3 = Actor("Angelina Jolie")
        actor4 = Actor(5)

        assert actor1.__eq__(actor2) == False
        assert actor3.__eq__(actor1) == True
        assert actor2.__eq__(actor4) == False

    def test_lt(self):
        actor1 = Actor("Angelina Jolie")
        actor2 = Actor("Brad Pitt")
        assert actor1.__lt__(actor2) == True

    def test_hash(self):
        actor1 = Actor("Angelina Jolie")
        assert actor1.__hash__() == hash("Angelina Jolie")

    def test_add_actor_colleague(self):
        actor1 = Actor("Angelina Jolie")
        actor2 = Actor("Brad Pitt")
        actor3 = Actor("Not an Actor")
        actor1.add_actor_colleague(actor2)

        assert actor1.get_number_of_colleagues() == 1
        assert actor2.get_number_of_colleagues() == 1

    def test_check_if_this_actor_worked_with(self):
        actor1 = Actor("Angelina Jolie")
        actor2 = Actor("Brad Pitt")
        actor3 = Actor("Not an Actor")
        actor1.add_actor_colleague(actor2)
        assert actor1.check_if_this_actor_worked_with(actor2) == True
        assert actor2.check_if_this_actor_worked_with(actor1) == True
        assert actor1.check_if_this_actor_worked_with(actor3) == False