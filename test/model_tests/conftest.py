import pytest
from peewee import SqliteDatabase

from boxwise_flask.models.models import Camps, Cms_Usergroups_Camps, Cms_Users
from boxwise_flask.models.qr_code import QRCode

MODELS = (Cms_Users, Cms_Usergroups_Camps, Camps, QRCode)


@pytest.fixture(autouse=True)
def setup_db():
    """fixture to setup database"""
    _db = SqliteDatabase(":memory:")
    with _db.bind_ctx(MODELS):
        _db.create_tables(MODELS)
        yield _db
        _db.drop_tables(MODELS)
