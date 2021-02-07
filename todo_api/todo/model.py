from datetime import datetime
from dataclasses import dataclass
from uuid import uuid4
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from todo_api.database import Model
from todo_api.database.mixins import TimestampMixin, UpdatableMixin


@dataclass
class Todo(Model, TimestampMixin, UpdatableMixin):
    __tablename__ = "todo"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: str = Column(String, nullable=False)
    due_at: datetime = Column(DateTime(timezone=True))
