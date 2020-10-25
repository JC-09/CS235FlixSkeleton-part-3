from flask import Blueprint, render_template
import CS235Flix.adapters.repository as repo
import CS235Flix.utilities.utilities as utilities
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from CS235Flix.movies.movies import SearchForm, SearchByTitleForm
from CS235Flix.movies.services import get_top_6_movies_by_revenue
import imdb
access = imdb.IMDb()
home_blueprint = Blueprint(
    'home_bp', __name__
)

@home_blueprint.route('/', methods=['GET'])
def home():
    top_6_picks = get_top_6_movies_by_revenue(repo=repo.repo_instance)

    for movie in top_6_picks:
        movie['view_review_url'] = url_for('home_bp.home')
        movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie=movie['id'])
        possible_movies = access.search_movie(movie['title'])
        movie['cover_url'] = possible_movies[0]['cover url']

    return render_template(
        'home/home.html',
        selected_movies=utilities.get_selected_movies(),
        top_6_picks=top_6_picks,
        genre_urls=utilities.get_genres_and_urls(),
        form=SearchForm(),
        handler_url=url_for('movies_bp.search'),
        title_form = SearchByTitleForm(),
        handler_url_title = url_for('movies_bp.search_by_title')
    )

