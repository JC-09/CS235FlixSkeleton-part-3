from CS235Flix.domainmodel.model import Movie, User





class MovieWatchingSimulation:
    def __init__(self, movie:Movie):
        self.__movie = None
        if isinstance(movie, Movie):
            self.__movie = movie
            self.__users = list()     # A list of user watching the movie
            self.__reviews = dict()  # A list of reviews (movie) made by this set of user for this particular movie
            self.__num_of_reviews = 0

    @property
    def movie(self):
        return self.__movie

    @property
    def users(self):
        return self.__users

    @property
    def reviews(self):
        return self.__reviews

    @property
    def num_of_reviews(self):
        return self.__num_of_reviews
    @property
    def number_of_users_watching(self):
        return len(self.__users)

    def add_user(self, user:User):
        if isinstance(user, User):
            if user not in self.__users:
                self.__users.append(user)
                user.watched_movies.append(self.movie)

    def retrieve_review(self):
        for user in self.__users:
            for review in user.reviews:
                if review.movie == self.__movie:
                    if user not in self.__reviews.keys():
                        self.__reviews[user] = [review]
                        self.__num_of_reviews+=1
                    else:
                        self.__reviews[user].append(review)
                        self.__num_of_reviews += 1

    def show_live_reviews(self):
        output_str = "Live Reviews for {}:\n".format(self.movie)

        for user in self.users:
            for review in self.__reviews[user]:
                output_str += "{}  --->  {}\n".format(user, review.review_text)
        return output_str

    def __repr__(self):
        return "Movie Watching Simulation - {} : {}\nNumber of users watching: {}\nNumber of reviews received: {}".format(self.movie.title,
                                                                                                                        self.movie.release_year,
                                                                                                                   self.number_of_users_watching,
                                                                                                                   self.num_of_reviews)

    def __eq__(self, other):
        return self.movie == other.movie



