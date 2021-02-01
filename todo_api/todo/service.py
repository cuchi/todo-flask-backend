from todo_api.database import db
from uuid import uuid4
from .model import Todo


class TodoService:
    def create(self, todo):
        created_todo = Todo(**todo)
        db.session.add(created_todo)
        db.session.commit()
        return created_todo

    def index(self):
        return Todo.query.all()
