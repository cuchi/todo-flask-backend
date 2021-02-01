from uuid import UUID
from todo_api.todo.service import TodoService

service = TodoService()


def test_if_service_exists():
    assert service is not None


def test_todo_creation(db_session):
    todos_count = len(service.index())
    assert todos_count == 0

    todo = service.create({"name": "Foo"})
    assert todo.name == "Foo"
    assert todo.id is not None
    assert todo.id.__class__ is UUID

    todos_count = len(service.index())
    assert todos_count == 1
