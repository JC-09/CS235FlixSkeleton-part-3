""" Initialize Flask App """

import os

from flask import Flask

import CS235Flix.adapters.repository as repo
from CS235Flix.adapters.memory_repository import MemoryRepository, populate

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool


def create_app(test_config=None):
    """ Construct the core application """

    # Create the Flask app object
    app = Flask(__name__)

    # Configure the app from configuration-file settings
    app.config.from_object('config.Config')
    data_path = os.path.join('CS235Flix', 'adapters', 'datafiles')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = MemoryRepository()
        populate(data_path, repo.repo_instance)

    elif app.config['REPOSITORY'] == 'database':
        # Configure database
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relatively to the application in covid-19.db
        # leading to a URI of "sqlite:///cs235flix.db"
        # Note that create_engine does not establish any actual DB connection directly!

        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri, connect_args={"check_same_thread":False}, poolclass=NullPool,
                                        echo=database_echo)




    # Build the application and register blueprints
    with app.app_context():

        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .movies import movies
        app.register_blueprint(movies.movies_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

    return app
