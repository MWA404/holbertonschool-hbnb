"""Amenity model module."""

from app import db
from app.models.base import BaseModel


class Amenity(BaseModel):
    """Represent an amenity stored in the database."""

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        """Initialize an amenity."""
        super().__init__()
        self.name = name
