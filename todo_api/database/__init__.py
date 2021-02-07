from flask_sqlalchemy import SQLAlchemy
from todo_api import app
from todo_api.config import DATABASE_URL

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Model = db.Model
