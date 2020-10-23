from sqlalchemy import select, inspect
from CS235Flix.adapters.orm import metadata


def test_database_populate_inspect_table_names(database_engine):
    # Get table information
    inspector = inspect(database_engine)
    all_table_names = inspector.get_table_names()

    assert all_table_names == ['actors', 'directors', 'genres', 'movie_actors', 'movie_directors', 'movie_genres', 'movies', 'reviews', 'users']
    assert len(all_table_names) == 9


def test_database_populate_select_all_genres(database_engine):
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['name'])
        print(all_genre_names)
        assert all_genre_names == ['Action', 'Adventure', 'Sci-Fi', 'Mystery', 'Horror', 'Thriller', 'Animation', 'Comedy', 'Family', 'Fantasy', 'Drama', 'Music', 'Biography', 'Romance']
        assert len(all_genre_names) == 14


def test_database_populate_select_all_users(database_engine):
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[-1]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['username'])

        assert all_users == ['thorke', 'fmercury', 'mjackson']


def test_database_populate_select_all_reviews(database_engine):
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[-2]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_comments = []
        for row in result:
            all_comments.append((row['id'], row['user_id'], row['movie_id'], row['review_text'], row['ratings']))

        assert all_comments == [(1, 2, 1, "This movie is great!", 8),
                                (2, 1, 1, "This movie is awesome", 9),
                                (3, 3, 1, "Love it!", 8)]


def test_database_populate_select_all_actor(database_engine):
    inspector = inspect(database_engine)
    name_of_actors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_actors_table]])
        result = connection.execute(select_statement)

        all_actors = []
        for row in result:
            all_actors.append(row['name'])
        assert all_actors == ['Chris Pratt', 'Vin Diesel', 'Bradley Cooper', 'Zoe Saldana', 'Noomi Rapace',
                              'Logan Marshall-Green', 'Michael Fassbender', 'Charlize Theron', 'James McAvoy',
                              'Anya Taylor-Joy', 'Haley Lu Richardson', 'Jessica Sula', 'Matthew McConaughey',
                              'Reese Witherspoon', 'Seth MacFarlane', 'Scarlett Johansson', 'Will Smith', 'Jared Leto',
                              'Margot Robbie', 'Viola Davis', 'Matt Damon', 'Tian Jing', 'Willem Dafoe', 'Andy Lau',
                              'Ryan Gosling', 'Emma Stone', 'Rosemarie DeWitt', 'J.K. Simmons', 'Essie Davis',
                              'Andrea Riseborough', 'Julian Barratt', 'Kenneth Branagh', 'Charlie Hunnam',
                              'Robert Pattinson', 'Sienna Miller', 'Tom Holland', 'Jennifer Lawrence', 'Michael Sheen',
                              'Laurence Fishburne']
        assert len(all_actors) == 39


def test_database_populate_select_all_director(database_engine):
    inspector = inspect(database_engine)
    name_of_directors_table = inspector.get_table_names()[1]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_directors_table]])
        result = connection.execute(select_statement)

        all_director = []
        for row in result:
            all_director.append(row['name'])
        assert all_director == ['James Gunn', 'Ridley Scott', 'M. Night Shyamalan', 'Christophe Lourdelet', 'David Ayer', 'Yimou Zhang', 'Damien Chazelle', 'Sean Foley', 'James Gray', 'Morten Tyldum']
        assert len(all_director) == 10


def test_database_populate_select_all_movies(database_engine):
    inspector = inspect(database_engine)
    name_of_movies_table = inspector.get_table_names()[-3]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_movies_table]])
        result = connection.execute(select_statement)

        all_movies = []
        for row in result:
            all_movies.append((row['id'], row['title']))

        assert len(all_movies) == 10
        assert all_movies[0] == (1, "Guardians of the Galaxy")
        assert all_movies[5] == (6, "The Great Wall")
        assert all_movies[9] == (10, "Passengers")












