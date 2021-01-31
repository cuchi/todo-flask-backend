from dataclasses import dataclass
from uuid import uuid4
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from todo_api.database import Base


@dataclass
class Todo(Base):
    __tablename__ = "todo"

    id: UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: str = Column(String)
