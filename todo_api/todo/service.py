from todo_api.database import db
from sqlalchemy.sql.expression import or_
from sqlalchemy import func
from uuid import uuid4
from .model import Todo


class TodoService:
    def create(self, **fields):
        todo = Todo(**fields)
        db.session.add(todo)
        db.session.commit()
        return todo

    def all(self, late=None, name=None):
        query = or_()
        if name is not None:
            query |= Todo.name.contains(name)
        if late is not None:
            now = func.now()
            query |= (
                Todo.due_at <= now if late else Todo.due_at > now or Todo.due_at is None
            )

        return Todo.query.filter(query).all()

    def update(self, id, **fields):
        todo = Todo.query.filter(Todo.id == id).first()
        todo.update(**fields)
        db.session.commit()
        return todo
