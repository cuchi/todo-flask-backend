from uuid import UUID
from todo_api.todo.service import TodoService

service = TodoService()


def test_todo_creation(db_session):
    todos_count = len(service.all())
    assert todos_count == 0

    todo = service.create(name="Foo")
    assert todo.name == "Foo"
    assert todo.id is not None
    assert todo.id.__class__ is UUID

    todos_count = len(service.all())
    assert todos_count == 1


def test_creation_timestamp(db_before):
    todo = service.create(name="Do something")
    assert todo.created_at >= db_before


def test_update_timestamp(db_before):
    todo = service.create(name="Do something")
    assert todo.updated_at is None

    updated_todo = service.update(todo.id, name="Do something else")
    assert updated_todo.updated_at >= todo.created_at
