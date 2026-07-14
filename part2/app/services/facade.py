import re

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    @staticmethod
    def _validate_user_data(user_data):
        """Validate user payload (models have no validation of their own)."""
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        email = user_data.get('email')

        if not first_name or not isinstance(first_name, str) \
                or len(first_name) > 50:
            raise ValueError("first_name is required (max 50 characters)")
        if not last_name or not isinstance(last_name, str) \
                or len(last_name) > 50:
            raise ValueError("last_name is required (max 50 characters)")
        if not email or not isinstance(email, str) \
                or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            raise ValueError("A valid email is required")

    @staticmethod
    def _validate_amenity_data(amenity_data):
        """Validate amenity payload."""
        name = amenity_data.get('name')
        if not name or not isinstance(name, str) or len(name) > 50:
            raise ValueError("name is required (max 50 characters)")

    def _validate_place_data(self, place_data, partial=False):
        """Validate place payload.

        When partial is True (PUT), only the provided fields are checked.
        """
        def has(field):
            return field in place_data

        if not partial or has('title'):
            title = place_data.get('title')
            if not title or not isinstance(title, str) or len(title) > 100:
                raise ValueError("title is required (max 100 characters)")

        if not partial or has('price'):
            price = place_data.get('price')
            if not isinstance(price, (int, float)) \
                    or isinstance(price, bool) or price < 0:
                raise ValueError("price must be a non-negative number")

        if not partial or has('latitude'):
            latitude = place_data.get('latitude')
            if not isinstance(latitude, (int, float)) \
                    or isinstance(latitude, bool) \
                    or not -90 <= latitude <= 90:
                raise ValueError("latitude must be between -90 and 90")

        if not partial or has('longitude'):
            longitude = place_data.get('longitude')
            if not isinstance(longitude, (int, float)) \
                    or isinstance(longitude, bool) \
                    or not -180 <= longitude <= 180:
                raise ValueError("longitude must be between -180 and 180")

        if not partial or has('owner_id'):
            owner = self.get_user(place_data.get('owner_id'))
            if not owner:
                raise ValueError("owner_id does not match any existing user")

        if has('amenities'):
            amenities = place_data.get('amenities')
            if not isinstance(amenities, list):
                raise ValueError("amenities must be a list of amenity IDs")
            for amenity_id in amenities:
                if not self.get_amenity(amenity_id):
                    raise ValueError(
                        "amenity '{}' does not exist".format(amenity_id))

    # ----------------------------- User -----------------------------------
    def create_user(self, user_data):
        self._validate_user_data(user_data)
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        # The repository has no get_by_attribute, so we scan get_all()
        return next(
            (u for u in self.user_repo.get_all() if u.email == email),
            None
        )

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        self._validate_user_data(user_data)
        return self.user_repo.update(user_id, user_data)

    # ---------------------------- Amenity ----------------------------------
    def create_amenity(self, amenity_data):
        self._validate_amenity_data(amenity_data)
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        self._validate_amenity_data(amenity_data)
        return self.amenity_repo.update(amenity_id, amenity_data)

    # ----------------------------- Place ------------------------------------
    def create_place(self, place_data):
        self._validate_place_data(place_data)
        data = dict(place_data)
        amenity_ids = data.pop('amenities', [])
        data.setdefault('description', "")
        place = Place(**data)
        place.amenity_ids = list(amenity_ids)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        self._validate_place_data(place_data, partial=True)
        data = dict(place_data)
        amenity_ids = data.pop('amenities', None)
        if amenity_ids is not None:
            place.amenity_ids = list(amenity_ids)
        return self.place_repo.update(place_id, data)
    # ----------------------------- Review -----------------------------------
    def _validate_review_data(self, review_data, partial=False):
        """Validate review payload."""
        def has(field):
            return field in review_data

        if not partial or has('text'):
            text = review_data.get('text')
            if not text or not isinstance(text, str):
                raise ValueError("text is required")

        if not partial or has('rating'):
            rating = review_data.get('rating')
            if not isinstance(rating, int) or isinstance(rating, bool) \
                    or not 1 <= rating <= 5:
                raise ValueError("rating must be an integer between 1 and 5")

        if not partial or has('user_id'):
            user = self.get_user(review_data.get('user_id'))
            if not user:
                raise ValueError("user_id does not match any existing user")

        if not partial or has('place_id'):
            place = self.get_place(review_data.get('place_id'))
            if not place:
                raise ValueError("place_id does not match any existing place")

    def create_review(self, review_data):
        self._validate_review_data(review_data)
        from app.models.review import Review
        review = Review(**review_data)
        self.review_repo.add(review)
        place = self.get_place(review_data['place_id'])
        if place and review.id not in place.review_ids:
            place.review_ids.append(review.id)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all()
                if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self._validate_review_data(review_data, partial=True)
        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            place = self.get_place(review.place_id)
            if place and review_id in place.review_ids:
                place.review_ids.remove(review_id)
            self.review_repo.delete(review_id)
        return review
