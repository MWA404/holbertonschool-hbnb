import uuid
from datetime import datetime

from app import db


class BaseModel(db.Model):
    """Base model containing common database attributes."""

    __abstract__ = True

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def save(self):
        """Update the updated_at timestamp to the current time."""
        self.updated_at = datetime.utcnow()

    def update(self, data):
        """Update attributes based on the provided dictionary."""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
