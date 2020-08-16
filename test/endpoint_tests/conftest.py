"""Functionality for common test setups.
See https://docs.pytest.org/en/stable/fixture.html#conftest-py-sharing-fixture-functions

In general, pass fixtures as arguments to a pytest test function in order to base the
test function on those fixtures. No additional import in the test module is required if
the fixture is defined in the 'conftest' module.

More details about the mechanism behind fixtures, and predefined fixtures at
https://docs.pytest.org/en/stable/fixture.html#pytest-fixtures-explicit-modular-scalable
"""

import os
import tempfile

import pytest

from boxwise_flask.app import create_app
from boxwise_flask.db import db
from boxwise_flask.models.models import Camps, Cms_Usergroups_Camps, Cms_Users, Person
from boxwise_flask.models.qr_code import QRCode

MODELS = (Person, Camps, Cms_Usergroups_Camps, Cms_Users, QRCode)


@pytest.fixture
def database():
    """Fixture for accessing the test database"""
    return db


@pytest.fixture()
def app(database):
    """Fixture providing a baseline for unit tests that rely on database operations via
    the Flask app. Adapted from
    https://flask.palletsprojects.com/en/1.1.x/testing/#the-testing-skeleton."""

    app = create_app()

    db_fd, db_filepath = tempfile.mkstemp(suffix=".sqlite3")
    app.config["DATABASE"] = {
        "name": db_filepath,
        "engine": "peewee.SqliteDatabase",
    }

    database.init_app(app)

    with database.database.bind_ctx(MODELS):
        database.database.create_tables(MODELS)
        database.close_db(None)
        with app.app_context():
            yield app

    database.close_db(None)
    os.close(db_fd)
    os.remove(db_filepath)


@pytest.fixture
def client(app):
    """The fixture simulates a client sending requests to the app."""
    client = app.test_client()
    return client
