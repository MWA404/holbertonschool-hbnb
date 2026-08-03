"""Place model module."""

from app import db
from app.models.base import BaseModel


class Place(BaseModel):
    """Represent a place stored in the database."""

    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(
        self,
        title,
        description,
        price,
        latitude,
        longitude,
        owner_id
    ):
        """Initialize a place."""
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

        # Relationships will be mapped in Task 8.
        self.owner_id = owner_id
        self.amenity_ids = []
        self.review_ids = []
