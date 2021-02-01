from flask_sqlalchemy import SQLAlchemy
from todo_api import app

engine_url = "postgresql://postgres:postgres@localhost:5432/postgres"
app.config["SQLALCHEMY_DATABASE_URI"] = engine_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Base = db.Model
