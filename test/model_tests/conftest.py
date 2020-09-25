"""Functionality for common test setups.
See https://docs.pytest.org/en/stable/fixture.html#conftest-py-sharing-fixture-functions

In general, pass fixtures as arguments to a pytest test function in order to base the
test function on those fixtures. No additional import in the test module is required if
the fixture is defined in the 'conftest' module.

More details about the mechanism behind fixtures, and predefined fixtures at
https://docs.pytest.org/en/stable/fixture.html#pytest-fixtures-explicit-modular-scalable
"""

import pytest
from peewee import SqliteDatabase

from boxwise_flask.models.base import Base
from boxwise_flask.models.box import Box
from boxwise_flask.models.qr import Qr
from boxwise_flask.models.user import User
from boxwise_flask.models.usergroup_base_access import UsergroupBaseAccess

MODELS = (User, UsergroupBaseAccess, Base, Qr, Box)


@pytest.fixture(autouse=True)
def setup_db_before_test():
    """Sets up database automatically before each test"""
    _db = SqliteDatabase(":memory:")
    with _db.bind_ctx(MODELS):
        _db.create_tables(MODELS)
        yield _db
        _db.drop_tables(MODELS)
