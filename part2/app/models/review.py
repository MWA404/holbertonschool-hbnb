from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place_id, user_id):
        super().__init__()
        self.text = text
        self.rating = rating      # Expected to be an integer between 1 and 5
        self.place_id = place_id  # Reference to the evaluated Place
        self.user_id = user_id    # Reference to the User who wrote the review
