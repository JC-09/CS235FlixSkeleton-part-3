# CS235Flix/movies/movies.py

from datetime import date
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.fields.html5 import SearchField, DecimalField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from CS235Flix.movies.services import NonExistentActorException, NonExistentDirectorException, NoSearchResultsException

import CS235Flix.adapters.repository as repo
import CS235Flix.utilities.utilities as utilities
import CS235Flix.movies.services as services

from CS235Flix.authentication.authentication import login_required


# Configure Blueprint
movies_blueprint = Blueprint(
    'movies_bp', __name__
)


@movies_blueprint.route('/movies_by_release_year', methods=['GET', 'POST'])
def movies_by_release_year():
    # Read query parameters
    target_year = request.args.get('year')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    earliest_year = services.get_earliest_year(repo=repo.repo_instance)
    latest_year = services.get_latest_year(repo=repo.repo_instance)

    if target_year is None:
        # No year query parameter, so return movies from the latest release year of the series
        target_year = latest_year
    else:
        # Convert target_year from string to int
        target_year = int(target_year)

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent movie id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int
        movie_to_show_reviews = int(movie_to_show_reviews)

    # Fetch movie(s) from the target year. This call also returns the previous and next release year for movies
    # immediately before and after the target year
    movies, previous_year, next_year = services.get_movies_by_release_year(target_year, repo.repo_instance)

    num_of_movies_found = len(movies)
    first_page_url = None
    # last_page_url = None
    previous_page_url = None
    next_page_url = None
    last_page_url = url_for('movies_bp.movies_by_release_year', year=earliest_year)  # year=int(oldest_movie['release_year'])
    first_page_url = url_for('movies_bp.movies_by_release_year', year=latest_year)  # int(latest_movie['release_year'])

    if num_of_movies_found > 0:
        previous_year = int(movies[0]['release_year']) - 1
        next_year = int(movies[0]['release_year']) + 1

        next_page_url = url_for('movies_bp.movies_by_release_year', year=previous_year)  # previous_year

        previous_page_url = url_for('movies_bp.movies_by_release_year', year=next_year)

        if previous_year < earliest_year:
            next_page_url = None

        if next_year > latest_year:
            previous_page_url = None

        # Construct urls for viewing movie reviews and adding reviews
        for movie in movies:
            movie['view_review_url'] = url_for('movies_bp.movies_by_release_year', year=target_year,
                                               view_reviews_for=movie['id'])
            movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['id'])

        # Generate the webpage to display the movie
        return render_template(
            'movies/movies.html',
            title='Movies',
            movies_title='Movies released in ' + str(target_year) + " - (" + str(num_of_movies_found) +  " results found)",
            movies=movies,
            form=SearchForm(),
            handler_url=url_for('movies_bp.search'),
            selected_movies=utilities.get_selected_movies(len(movies) * 2),
            genre_urls=utilities.get_genres_and_urls(),
            first_page_url=first_page_url,
            last_page_url=last_page_url,
            previous_page_url=previous_page_url,
            next_page_url=next_page_url,
            show_reviews_for_movie=movie_to_show_reviews,
            title_form=SearchByTitleForm(),
            handler_url_title=url_for('movies_bp.search_by_title'),
        )

    # No movies to show, so return the homepage
    return redirect(url_for('home_bp.home'))


@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    movies_per_page = 10

    # Read query parameter.
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')
    movie_to_show_reviews = request.args.get('view_reviews_for')

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent article id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int
        movie_to_show_reviews = int(movie_to_show_reviews)

    if cursor is None:
        # None cursor query parameter, so initialise cursor to start the begining
        cursor = 0
    else:
        # Convert cursor from string to int
        cursor = int(cursor)

    # Retrieve movie ids for movies that are classified with genre_name
    movie_ids = services.get_movie_ids_for_genre(genre_name, repo.repo_instance)
    num_of_movies_found = len(movie_ids)

    # Retrieve the batch of articles to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_page_url = None
    last_page_url = None
    previous_page_url = None
    next_page_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        previous_page_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_page_url = url_for('movies_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and last navigation buttons.
        next_page_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page

        last_page_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)

    # Construct urls for viewing movie reviews and adding reviews
    for movie in movies:
        movie['view_review_url'] = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor,
                                           view_reviews_for=movie['id'])
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['id'])
    print(cursor)
    current_page = cursor
    if current_page + 10 < num_of_movies_found:
        current_page += 10
    else:
        current_page += (num_of_movies_found - current_page)

    # Generate the webpage to display the movies
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Movies classified as ' + genre_name + " - (showing " + str(current_page) + " of " +  str(num_of_movies_found) + " results)",
        movies=movies,
        form=SearchForm(),
        handler_url=url_for('movies_bp.search'),
        selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_page_url=first_page_url,
        last_page_url=last_page_url,
        previous_page_url=previous_page_url,
        next_page_url=next_page_url,
        show_reviews_for_movie=movie_to_show_reviews,
        title_form=SearchByTitleForm(),
        handler_url_title=url_for('movies_bp.search_by_title'),
    )


@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an movie id, when subsequently called with a HTTP POST request, the movie id remains in the form

    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the movie id, representing the reviewed movie, from the form.
        movie_id = int(form.movie_id.data)
        rating = int(form.rating.data)

        # Use the service layer to store the new review
        services.add_review(form.review.data, username, movie_id, rating, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)
        release_year = movie['release_year']
        # genre_name = movie['genres'][0]
        print(movie['reviews'][0]['timestamp'])
        # Cause the web browser to display the page of all movies that have the same genre as the reviewed movie, and
        # display all reviews, including the new review.

        # return redirect(url_for('movies_bp.movies_by_release_year', year=release_year, view_reviews_for=movie_id))
        return redirect(url_for('movies_bp.search_movies_by_title', title=movie['title']))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie id, representing the movie to review, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie'))

        # Store the movie id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the article id of the article being commented from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page include a form object.
    movie = services.get_movie(movie_id, repo.repo_instance)

    return render_template(
        'movies/review_on_movie.html',
        title='Edit movie',
        movie=movie,
        form_review=form,
        form=SearchForm(),
        handler_url_review=url_for('movies_bp.review_on_movie'),
        handler_url=url_for("movies_bp.search"),
        selected_movies=utilities.get_selected_movies(),
        genre_urls=utilities.get_genres_and_urls(),
        title_form=SearchByTitleForm(),
        handler_url_title=url_for('movies_bp.search_by_title'),
    )


@movies_blueprint.route('/search_movies_by_actor_and_or_director', methods=['GET'])
def search_movies_by_actor_and_or_director():
    # Read query parameters
    target_actor = request.args.get('actor')
    target_director = request.args.get('director')
    movie_to_show_reviews = request.args.get('view_reviews_for')
    movies = list()
    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent article id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int
        movie_to_show_reviews = int(movie_to_show_reviews)

    title_message = "No results found"
    if target_actor is None:
        target_actor = ""
    if target_director is None:
        target_director = ""
    if len(target_director) == 0 and len(target_actor) != 0:
        title_message = "Movies played by " + target_actor
        try:
            movies = services.search_movie_by_actor_fullname(actor_fullname=target_actor, repo=repo.repo_instance)
        except NonExistentActorException:
            pass
    elif len(target_director) != 0 and len(target_actor) == 0:
        title_message = "Movies directed by " + target_director
        try:
            movies = services.search_movie_directed_by_director_fullname(director_fullname=target_director,
                                                                         repo=repo.repo_instance)
        except NonExistentDirectorException:
            pass
    elif len(target_director) != 0 and len(target_actor) != 0:
        title_message = "Movies played by " + target_actor + ", and directed by " + target_director
        try:
            movies = services.search_movie_by_actor_and_director(actor_fullname=target_actor,
                                                                 director_fullname=target_director,
                                                                 repo=repo.repo_instance)
        except NoSearchResultsException:
            pass
    first_page_url = None
    last_page_url = None
    previous_page_url = None
    next_page_url = None

    # There is at least one movie played by the target actor
    for movie in movies:
        movie['view_review_url'] = url_for('movies_bp.search_movies_by_actor_and_or_director', actor=target_actor,
                                           view_reviews_for=movie['id'])
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['id'])

    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title=title_message + " - (" + str(len(movies)) + " results found)",
        movies=movies,
        form=SearchForm(),
        handler_url=url_for('movies_bp.search'),
        selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_page_url=first_page_url,
        last_page_url=last_page_url,
        previous_page_url=previous_page_url,
        next_page_url=next_page_url,
        show_reviews_for_movie=movie_to_show_reviews,
        title_form=SearchByTitleForm(),
        handler_url_title=url_for('movies_bp.search_by_title'),
    )


@movies_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    if form.validate_on_submit():
        # Successful POST
        actor_fullname = form.actor.data

        director_fullname = form.director.data

        return redirect(url_for('movies_bp.search_movies_by_actor_and_or_director', actor=actor_fullname, director=director_fullname))

    return render_template(
        'search.html',
        title='Search Movie',
        form=form,
        handler_url=url_for('movies_bp.search'),
        handler_url_review=url_for('movies_bp.review_on_movie'),
        title_form=SearchByTitleForm(),
        handler_url_title=url_for('movies_bp.search_by_title'),
    )


@movies_blueprint.route('/search_movies_by_title', methods=['GET'])
def search_movies_by_title():
    target_title = request.args.get('title')
    movie_to_show_reviews = request.args.get('view_reviews_for')
    movies = list()

    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent article id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int
        movie_to_show_reviews = int(movie_to_show_reviews)

    if target_title is None:
        target_title = ""

    try:
        movies = services.search_movie_by_title(title=target_title, repo=repo.repo_instance)
    except NoSearchResultsException:
        pass

    first_page_url = None
    last_page_url = None
    previous_page_url = None
    next_page_url = None

    for movie in movies:
        movie['view_review_url'] = url_for('movies_bp.search_movies_by_title', title=target_title,
                                           view_reviews_for=movie['id'])
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['id'])

    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Search results of "' + target_title + '" - (' + str(len(movies)) + ' results found)',
        movies=movies,
        form=SearchForm(),
        handler_url=url_for('movies_bp.search'),
        selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_page_url=first_page_url,
        last_page_url=last_page_url,
        previous_page_url=previous_page_url,
        next_page_url=next_page_url,
        show_reviews_for_movie=movie_to_show_reviews,
        title_form=SearchByTitleForm(),
        handler_url_title=url_for('movies_bp.search_by_title')
    )


@movies_blueprint.route('/search_by_title', methods=['GET', 'POST'])
def search_by_title():
    title_form = SearchByTitleForm()
    if title_form.validate_on_submit():
        # Successful POST
        title = title_form.title.data

        return redirect(url_for('movies_bp.search_movies_by_title', title=title))

    return render_template(
        'search.html',
        title='Search Movie',
        form=SearchForm(),
        title_form=title_form,
        handler_url_title=url_for('movies_bp.search_by_title'),
        handler_url=url_for('movies_bp.search'),
        handler_url_review=url_for('movies_bp.review_on_movie'),
    )


@movies_blueprint.route('/suggest', methods=['GET'])
@login_required
def suggest_movie():
    # Obtain the username of the currenlty logged in user.
    username = session['username']
    suggestions = services.get_suggestions_for_a_user(username=username, repo=repo.repo_instance)
    num_of_suggested_movies = len(suggestions)
    title_message = "Oops! You haven't reviewed any movies yet, please review some movies you like and we will have recommendations for you."
    if num_of_suggested_movies > 0:
        title_message = "Based on your reviews, we recommend the following " + str(num_of_suggested_movies) + " movies to you. Enjoy!"

    movie_to_show_reviews = request.args.get('view_reviews_for')
    if movie_to_show_reviews is None:
        # No view-reviews query parameter, so set to a non-existent article id.
        movie_to_show_reviews = -1
    else:
        # Convert movie_to_show_reviews from string to int
        movie_to_show_reviews = int(movie_to_show_reviews)

    first_page_url = None
    last_page_url = None
    previous_page_url = None
    next_page_url = None

    for movie in suggestions:
        movie['view_review_url'] = url_for('movies_bp.suggest_movie',
                                           view_reviews_for=movie['id'])
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['id'])

    return render_template(
        "movies/movies.html",
        title='Movies',
        movies=suggestions,
        movies_title=title_message,
        form=SearchForm(),
        handler_url=url_for('movies_bp.search'),
        selected_movies=utilities.get_selected_movies(len(suggestions) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_page_url=first_page_url,
        last_page_url=last_page_url,
        previous_page_url=previous_page_url,
        next_page_url=next_page_url,
        show_reviews_for_movie=movie_to_show_reviews,
        title_form=SearchByTitleForm(),
        handler_url_title=url_for('movies_bp.search_by_title'),
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review:', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    rating = DecimalField('Please leave a rating from 1 to 10:', validators=[
        DataRequired(message='You must enter a number'),
        NumberRange(min=1, max=10, message='Your rating must be within the valid range (1 - 10)'),
    ])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    actor = SearchField('Please enter actor fullname')
    director = SearchField('Please enter director fullname')
    search = SubmitField('Search')


class SearchByTitleForm(FlaskForm):
    title = SearchField('Please enter movie title')
    search = SubmitField('Search')
