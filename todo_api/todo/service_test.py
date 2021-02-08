from uuid import UUID
from datetime import datetime, timedelta
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


def test_late_todos(db_session, faker):
    now = datetime.utcnow()
    one_hour = timedelta(hours=1)
    for _ in range(3):
        service.create(name=faker.text())
    for _ in range(3):
        service.create(name=faker.text(), due_at=now - one_hour)
    for _ in range(3):
        service.create(name=faker.text(), due_at=now + one_hour)

    assert len(service.all()) == 9
    assert len(service.all(late=True)) == 3
    assert len(service.all(late=False)) == 6


def test_name_search(db_session):
    service.create(name="Do something")
    service.create(name="Do something again")
    service.create(name="Do the other thing")

    result = service.all(name="something")

    assert len(result) == 2
