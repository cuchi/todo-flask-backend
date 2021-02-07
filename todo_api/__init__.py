from flask import Flask
from flask_uuid import FlaskUUID

app = Flask(__name__)
FlaskUUID(app)


import todo_api.database
import todo_api.controllers

if __name__ == "__main__":
    app.run()
