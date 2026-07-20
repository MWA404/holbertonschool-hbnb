import unittest
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.services.facade import HBnBFacade


class TestUserModel(unittest.TestCase):
    def test_user_creation(self):
        user = User(first_name="John", last_name="Doe", email="john@test.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.email, "john@test.com")

    def test_user_has_id(self):
        user = User(first_name="A", last_name="B", email="a@b.com")
        self.assertIsNotNone(user.id)


class TestPlaceModel(unittest.TestCase):
    def test_place_creation(self):
        place = Place(title="Nice", description="Cozy", price=100.0,
                      latitude=40.0, longitude=-70.0, owner_id="oid")
        self.assertEqual(place.title, "Nice")

    def test_place_has_empty_lists(self):
        place = Place(title="X", description="Y", price=1.0,
                      latitude=0.0, longitude=0.0, owner_id="oid")
        self.assertEqual(place.amenity_ids, [])
        self.assertEqual(place.review_ids, [])


class TestReviewModel(unittest.TestCase):
    def test_review_creation(self):
        review = Review(text="Great", rating=5,
                        place_id="pid", user_id="uid")
        self.assertEqual(review.text, "Great")
        self.assertEqual(review.rating, 5)


class TestAmenityModel(unittest.TestCase):
    def test_amenity_creation(self):
        amenity = Amenity(name="WiFi")
        self.assertEqual(amenity.name, "WiFi")

    def test_amenity_has_id(self):
        amenity = Amenity(name="Pool")
        self.assertIsNotNone(amenity.id)


class TestUserValidation(unittest.TestCase):
    def setUp(self):
        self.facade = HBnBFacade()

    def test_valid_user(self):
        user = self.facade.create_user({
            "first_name": "Jane", "last_name": "Doe", "email": "j@t.com"})
        self.assertIsNotNone(user.id)

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            self.facade.create_user({
                "first_name": "A", "last_name": "B", "email": "not-email"})

    def test_missing_first_name(self):
        with self.assertRaises(ValueError):
            self.facade.create_user({
                "first_name": "", "last_name": "B", "email": "a@b.com"})

    def test_first_name_too_long(self):
        with self.assertRaises(ValueError):
            self.facade.create_user({
                "first_name": "A" * 51, "last_name": "B",
                "email": "a@b.com"})


class TestPlaceValidation(unittest.TestCase):
    def setUp(self):
        self.facade = HBnBFacade()
        user = self.facade.create_user({
            "first_name": "O", "last_name": "T", "email": "o@t.com"})
        self.owner_id = user.id

    def test_valid_place(self):
        place = self.facade.create_place({
            "title": "T", "description": "T", "price": 100.0,
            "latitude": 40.0, "longitude": -70.0,
            "owner_id": self.owner_id, "amenities": []})
        self.assertIsNotNone(place.id)

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            self.facade.create_place({
                "title": "T", "description": "T", "price": -1.0,
                "latitude": 0.0, "longitude": 0.0,
                "owner_id": self.owner_id, "amenities": []})

    def test_invalid_latitude(self):
        with self.assertRaises(ValueError):
            self.facade.create_place({
                "title": "T", "description": "T", "price": 1.0,
                "latitude": 999.0, "longitude": 0.0,
                "owner_id": self.owner_id, "amenities": []})

    def test_invalid_longitude(self):
        with self.assertRaises(ValueError):
            self.facade.create_place({
                "title": "T", "description": "T", "price": 1.0,
                "latitude": 0.0, "longitude": 999.0,
                "owner_id": self.owner_id, "amenities": []})

    def test_invalid_owner(self):
        with self.assertRaises(ValueError):
            self.facade.create_place({
                "title": "T", "description": "T", "price": 1.0,
                "latitude": 0.0, "longitude": 0.0,
                "owner_id": "no-id", "amenities": []})


class TestAmenityValidation(unittest.TestCase):
    def setUp(self):
        self.facade = HBnBFacade()

    def test_valid_amenity(self):
        amenity = self.facade.create_amenity({"name": "WiFi"})
        self.assertIsNotNone(amenity.id)

    def test_empty_amenity_name(self):
        with self.assertRaises(ValueError):
            self.facade.create_amenity({"name": ""})

    def test_amenity_name_too_long(self):
        with self.assertRaises(ValueError):
            self.facade.create_amenity({"name": "X" * 51})


class TestReviewValidation(unittest.TestCase):
    def setUp(self):
        self.facade = HBnBFacade()
        user = self.facade.create_user({
            "first_name": "U", "last_name": "T", "email": "u@t.com"})
        self.user_id = user.id
        place = self.facade.create_place({
            "title": "P", "description": "D", "price": 1.0,
            "latitude": 0.0, "longitude": 0.0,
            "owner_id": self.user_id, "amenities": []})
        self.place_id = place.id

    def test_valid_review(self):
        review = self.facade.create_review({
            "text": "Great", "rating": 5,
            "user_id": self.user_id, "place_id": self.place_id})
        self.assertIsNotNone(review.id)

    def test_empty_text(self):
        with self.assertRaises(ValueError):
            self.facade.create_review({
                "text": "", "rating": 5,
                "user_id": self.user_id, "place_id": self.place_id})

    def test_rating_too_high(self):
        with self.assertRaises(ValueError):
            self.facade.create_review({
                "text": "T", "rating": 6,
                "user_id": self.user_id, "place_id": self.place_id})

    def test_rating_too_low(self):
        with self.assertRaises(ValueError):
            self.facade.create_review({
                "text": "T", "rating": 0,
                "user_id": self.user_id, "place_id": self.place_id})

    def test_invalid_user_id(self):
        with self.assertRaises(ValueError):
            self.facade.create_review({
                "text": "T", "rating": 5,
                "user_id": "no-user", "place_id": self.place_id})

    def test_invalid_place_id(self):
        with self.assertRaises(ValueError):
            self.facade.create_review({
                "text": "T", "rating": 5,
                "user_id": self.user_id, "place_id": "no-place"})


if __name__ == '__main__':
    unittest.main()
