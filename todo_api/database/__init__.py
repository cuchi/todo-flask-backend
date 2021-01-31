from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine_url = "postgresql://postgres:postgres@localhost:5432/postgres"

engine = create_engine(engine_url)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import todo_api.models

    Base.metadata.create_all(bind=engine)
