from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id  # Reference to the User who owns the place
        self.amenity_ids = []     # List of Amenity IDs available at this place
        self.review_ids = []      # List of Review IDs linked to this place
