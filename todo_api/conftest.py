import pytest
import re
import sqlalchemy.pool.base

from sqlalchemy import func, create_engine
from flask_sqlalchemy import SQLAlchemy
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

from todo_api import app as todo_app
from todo_api.config import DATABASE_URL


def _reset(self, pool):
    return pool._dialect.do_rollback(self)


sqlalchemy.pool.base._ConnectionFairy._reset = _reset


def create_testing_db(connection):
    connection.execute("DROP DATABASE IF EXISTS test")
    connection.execute("CREATE DATABASE test")


def drop_testing_db(connection):
    connection.execute(
        """
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = 'test'
            AND pid <> pg_backend_pid();
        """
    )
    connection.execute("DROP DATABASE test")


@pytest.fixture(scope="session")
def app():
    return todo_app


@pytest.fixture(scope="session")
def _db(app):
    connection = create_engine(DATABASE_URL).connect()
    connection.connection.connection.set_isolation_level(0)
    create_testing_db(connection)

    test_database_url = re.sub(r"/[^/]*$", "/test", DATABASE_URL)
    app.config["SQLALCHEMY_DATABASE_URI"] = test_database_url

    alembic_config = AlembicConfig("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", test_database_url)
    alembic_upgrade(alembic_config, "head")

    yield SQLAlchemy(app=app)

    drop_testing_db(connection)
    connection.close()


@pytest.fixture(scope="function")
def db_before(db_session):
    return db_session.query(func.now()).first()[0]
