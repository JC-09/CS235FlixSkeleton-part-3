
import csv

from CS235Flix.domainmodel.model import Movie, Actor, Genre, Director


class MovieFileCSVReader:

    def __init__(self, file_name: str):
        self.__file_name = file_name
        self.__dataset_of_movies = list()
        self.__dataset_of_actors = list()
        self.__dataset_of_directors = list()
        self.__dataset_of_genres = list()

        #--- Further Extension ---#
        self.__dataset_of_runtime = list()
        self.__dataset_of_description = list()
        self.__dataset_of_ratings = list()
        self.__dataset_of_votes = list()
        self.__dataset_of_revenue = list()
        self.__dataset_of_metadata = list()


    def read_csv_file(self):
        duplicated_genre = []
        duplicated_actors = []
        with open(self.__file_name, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)
            for row in movie_file_reader:
                # Append to the movie data set
                title = row['Title']
                year = int(row['Year'])
                movie = Movie(title, year, 4)
                if (movie not in self.__dataset_of_movies):
                    self.__dataset_of_movies.append(movie)
                # Store potential duplicated actors
                duplicated_actors.append(row['Actors'].split(','))  # This is a list of list

                # Store unique directors
                director = Director(row['Director'])
                if director not in self.__dataset_of_directors:
                    self.__dataset_of_directors.append(director)

                # Store potential duplicated genres
                duplicated_genre.append(row['Genre'].split(','))

                #Store description
                description = row['Description']
                self.__dataset_of_description.append(description)


                # Store runtime
                runtime = row['Runtime (Minutes)']
                try:
                    runtime = int(runtime)
                    self.__dataset_of_runtime.append(runtime)
                except ValueError:
                    continue

                # Store ratings
                rating = row['Rating']
                try:
                    rating = float(rating)
                    self.__dataset_of_ratings.append(rating)
                except ValueError:
                    continue

                # Store votes
                vote = row['Votes']
                try:
                    vote = int(vote)
                    self.__dataset_of_votes.append(vote)
                except ValueError:
                    continue

                # Store revenue
                revenue = row["Revenue (Millions)"]
                try:
                    revenue = float(revenue)
                    self.__dataset_of_revenue.append(revenue)
                except ValueError:
                    continue

                # Store Metascore
                meta_score = row["Metascore"]
                try:
                    meta_score = float(meta_score)
                    self.__dataset_of_metadata.append(meta_score)
                except ValueError:
                    continue



        for actor_list in duplicated_actors:
            for current_actor in actor_list:
                current_actor = Actor(current_actor)
                if current_actor not in self.__dataset_of_actors:
                    self.__dataset_of_actors.append(current_actor)

        for genre_list in duplicated_genre:
            for current_genre in genre_list:
                current_genre = Genre(current_genre)
                if current_genre not in self.__dataset_of_genres:
                    self.__dataset_of_genres.append(current_genre)

    @property
    def dataset_of_movies(self):
        return self.__dataset_of_movies

    @property
    def dataset_of_actors(self):
        return self.__dataset_of_actors

    @property
    def dataset_of_directors(self):
        return self.__dataset_of_directors

    @property
    def dataset_of_genres(self):
        return self.__dataset_of_genres

    @property
    def dataset_of_runtime(self):
        return self.__dataset_of_runtime
    @property
    def dataset_of_description(self):
        return self.__dataset_of_description

    @property
    def dataset_of_ratings(self):
        return self.__dataset_of_ratings

    @property
    def dataset_of_votes(self):
        return self.__dataset_of_votes

    @property
    def dataset_of_revenue(self):
        return self.__dataset_of_revenue

    @property
    def dataset_of_metadata(self):
        return self.__dataset_of_metadata