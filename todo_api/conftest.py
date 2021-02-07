import pytest
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.pool.base

from todo_api import app as todo_app


def _reset(self, pool):
    return pool._dialect.do_rollback(self)


sqlalchemy.pool.base._ConnectionFairy._reset = _reset


@pytest.fixture(scope="session")
def app():
    return todo_app


@pytest.fixture(scope="session")
def _db(app):
    return SQLAlchemy(app=app)


@pytest.fixture(scope="function")
def db_before(db_session):
    return db_session.query(func.now()).first()[0]
