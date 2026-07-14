import unittest
from app import create_app


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for the review endpoints."""

    def setUp(self):
        """Set up test client and create a user and place."""
        import uuid
        self.app = create_app()
        self.client = self.app.test_client()

        unique_email = "test-{}@example.com".format(uuid.uuid4())
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": unique_email
        })
        self.user_id = user_response.get_json()['id']

        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A test place",
            "price": 100.0,
            "latitude": 40.0,
            "longitude": -70.0,
            "owner_id": self.user_id,
            "amenities": []
        })
        self.place_id = place_response.get_json()['id']

    def test_create_review_valid(self):
        """Test creating a review with valid data."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['text'], "Great place!")
        self.assertEqual(data['rating'], 5)

    def test_create_review_empty_text(self):
        """Test creating a review with empty text."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating(self):
        """Test creating a review with invalid rating."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice place",
            "rating": 10,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user(self):
        """Test creating a review with non-existent user."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice",
            "rating": 4,
            "user_id": "invalid-id",
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_place(self):
        """Test creating a review with non-existent place."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": "invalid-id"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        """Test getting all reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_review_by_id(self):
        """Test getting a review by ID."""
        create = self.client.post('/api/v1/reviews/', json={
            "text": "Good",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create.get_json()['id']
        response = self.client.get('/api/v1/reviews/{}'.format(review_id))
        self.assertEqual(response.status_code, 200)

    def test_get_review_not_found(self):
        """Test getting a non-existent review."""
        response = self.client.get('/api/v1/reviews/invalid-id')
        self.assertEqual(response.status_code, 404)

    def test_update_review(self):
        """Test updating a review."""
        create = self.client.post('/api/v1/reviews/', json={
            "text": "Ok",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create.get_json()['id']
        response = self.client.put(
            '/api/v1/reviews/{}'.format(review_id),
            json={"text": "Updated", "rating": 5}
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_review(self):
        """Test deleting a review."""
        create = self.client.post('/api/v1/reviews/', json={
            "text": "Delete me",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create.get_json()['id']
        response = self.client.delete('/api/v1/reviews/{}'.format(review_id))
        self.assertEqual(response.status_code, 200)

    def test_delete_review_not_found(self):
        """Test deleting a non-existent review."""
        response = self.client.delete('/api/v1/reviews/invalid-id')
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_by_place(self):
        """Test getting all reviews for a specific place."""
        self.client.post('/api/v1/reviews/', json={
            "text": "Nice",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        response = self.client.get(
            '/api/v1/reviews/places/{}/reviews'.format(self.place_id))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
