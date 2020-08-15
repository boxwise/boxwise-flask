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
    return db


@pytest.fixture()
def app(database):
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
    client = app.test_client()
    return client
