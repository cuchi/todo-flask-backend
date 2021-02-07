from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import Column, DateTime, func


@dataclass
class TimestampMixin(object):
    created_at: datetime = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: datetime = Column(DateTime(timezone=True), onupdate=func.now())


class UpdatableMixin:
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
