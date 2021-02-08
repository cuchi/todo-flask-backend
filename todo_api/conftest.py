import pytest
import re
import sqlalchemy.pool.base

from time import sleep
from uuid import uuid4
from sqlalchemy import func, create_engine
from flask_sqlalchemy import SQLAlchemy
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig

from todo_api import app as todo_app
from todo_api.config import DATABASE_URL

TEMPLATE_DB_NAME = "test_template"


def _reset(self, pool):
    return pool._dialect.do_rollback(self)


sqlalchemy.pool.base._ConnectionFairy._reset = _reset


def get_url_for_db(db_name):
    return re.sub(r"/[^/]*$", f"/{db_name}", DATABASE_URL)


def create_db(connection, db_name, template_name="template0"):
    connection.execute(f"DROP DATABASE IF EXISTS {db_name}")
    connection.execute(f"CREATE DATABASE {db_name} TEMPLATE {template_name}")


def drop_db(connection, db_name):
    connection.execute(
        """
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '{db_name}'
            AND pid <> pg_backend_pid();
        """.format(
            db_name=db_name
        )
    )
    connection.execute(f"DROP DATABASE {db_name}")


@pytest.fixture(scope="session")
def app():
    return todo_app


@pytest.fixture(scope="session")
def template_db(worker_id):
    if worker_id != "master":
        return

    connection = create_engine(DATABASE_URL).connect()
    connection.connection.connection.set_isolation_level(0)
    create_db(connection, TEMPLATE_DB_NAME)
    connection.close()
    alembic_config = AlembicConfig("alembic.ini")
    alembic_config.set_main_option("sqlalchemy.url", get_url_for_db(TEMPLATE_DB_NAME))
    alembic_upgrade(alembic_config, "head")


@pytest.fixture(scope="session")
def _db(app, template_db):
    test_db_name = f"test_{uuid4()}".replace("-", "_")

    connection = create_engine(DATABASE_URL).connect()
    connection.connection.connection.set_isolation_level(0)
    create_db(connection, test_db_name, template_name=TEMPLATE_DB_NAME)

    app.config["SQLALCHEMY_DATABASE_URI"] = get_url_for_db(test_db_name)
    yield SQLAlchemy(app=app)

    drop_db(connection, test_db_name)
    connection.close()


@pytest.fixture(scope="function")
def db_before(db_session):
    return db_session.query(func.now()).first()[0]
