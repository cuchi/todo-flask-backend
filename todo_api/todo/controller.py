from flask import g, jsonify
from flask_expects_json import expects_json
from todo_api import app
from todo_api.todo.service import TodoService

service = TodoService()

todo_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
    },
    "required": ["name"],
}


@app.route("/todos", methods=["POST"])
@expects_json(todo_schema)
def create():
    return jsonify(service.create(g.data))


@app.route("/todos", methods=["GET"])
def index():
    return jsonify(service.index())
