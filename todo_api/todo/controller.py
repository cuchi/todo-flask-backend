from flask import jsonify
from webargs import fields
from webargs.flaskparser import use_kwargs
from todo_api import app
from todo_api.todo.service import TodoService

service = TodoService()


@app.route("/todos", methods=["POST"])
@use_kwargs({"name": fields.String(required=True), "due_at": fields.DateTime()})
def post(**kwargs):
    return jsonify(service.create(**kwargs)), 201


@app.route("/todos", methods=["GET"])
@use_kwargs({"name": fields.String(), "late": fields.Boolean()}, location="query")
def get(**kwargs):
    return jsonify(service.all(**kwargs))


@app.route("/todos/<uuid:id>", methods=["PATCH"])
@use_kwargs({"name": fields.String(), "due_at": fields.DateTime()})
def patch(id, **kwargs):
    return jsonify(service.update(id, **kwargs))
