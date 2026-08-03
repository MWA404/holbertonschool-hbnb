"""Review model module."""

from app import db
from app.models.base import BaseModel


class Review(BaseModel):
    """Represent a review stored in the database."""

    __tablename__ = 'reviews'

    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(
        db.String(36),
        db.ForeignKey('places.id'),
        nullable=False
    )
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id'),
        nullable=False
    )

    def __init__(self, text, rating, place_id, user_id):
        """Initialize a review."""
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
