# Testing Report - HBnB Part 2

This document describes the testing approach and results for the HBnB Evolution API.

## Testing Strategy

Testing is performed at two levels:

1. **Unit tests** (`tests/test_models.py`) — Test models and business logic validation directly.
2. **Integration tests** (`tests/test_reviews.py`) — Test the API endpoints end-to-end using Flask's test client.

## Running the Tests

```bash
python3 -m unittest discover tests
```

## Test Results Summary

| Test File | Tests | Status |
|---|---|---|
| test_models.py | 24 | All Pass |
| test_reviews.py | 12 | All Pass |

## Review Endpoints Tests

| # | Endpoint | Method | Payload | Expected | Actual | Result |
|---|---|---|---|---|---|---|
| 1 | /api/v1/reviews/ | POST | Valid data | 201 | 201 | Pass |
| 2 | /api/v1/reviews/ | POST | Empty text | 400 | 400 | Pass |
| 3 | /api/v1/reviews/ | POST | Rating > 5 | 400 | 400 | Pass |
| 4 | /api/v1/reviews/ | POST | Invalid user_id | 400 | 400 | Pass |
| 5 | /api/v1/reviews/ | POST | Invalid place_id | 400 | 400 | Pass |
| 6 | /api/v1/reviews/ | GET | - | 200 | 200 | Pass |
| 7 | /api/v1/reviews/<id> | GET | Valid id | 200 | 200 | Pass |
| 8 | /api/v1/reviews/<id> | GET | Invalid id | 404 | 404 | Pass |
| 9 | /api/v1/reviews/<id> | PUT | Valid update | 200 | 200 | Pass |
| 10 | /api/v1/reviews/<id> | DELETE | Valid id | 200 | 200 | Pass |
| 11 | /api/v1/reviews/<id> | DELETE | Invalid id | 404 | 404 | Pass |
| 12 | /api/v1/places/<id>/reviews | GET | Valid place | 200 | 200 | Pass |

## Model Validation Tests

| # | Model | Test | Expected | Actual | Result |
|---|---|---|---|---|---|
| 1 | User | Valid creation | User created | User created | Pass |
| 2 | User | Has id | id present | id present | Pass |
| 3 | User | Invalid email format | ValueError | ValueError | Pass |
| 4 | User | Empty first_name | ValueError | ValueError | Pass |
| 5 | User | first_name > 50 chars | ValueError | ValueError | Pass |
| 6 | Place | Valid creation | Place created | Place created | Pass |
| 7 | Place | Empty lists | Empty | Empty | Pass |
| 8 | Place | Negative price | ValueError | ValueError | Pass |
| 9 | Place | Latitude out of range | ValueError | ValueError | Pass |
| 10 | Place | Longitude out of range | ValueError | ValueError | Pass |
| 11 | Place | Invalid owner_id | ValueError | ValueError | Pass |
| 12 | Review | Valid creation | Review created | Review created | Pass |
| 13 | Review | Empty text | ValueError | ValueError | Pass |
| 14 | Review | Rating > 5 | ValueError | ValueError | Pass |
| 15 | Review | Rating < 1 | ValueError | ValueError | Pass |
| 16 | Review | Invalid user_id | ValueError | ValueError | Pass |
| 17 | Review | Invalid place_id | ValueError | ValueError | Pass |
| 18 | Amenity | Valid creation | Amenity created | Amenity created | Pass |
| 19 | Amenity | Has id | id present | id present | Pass |
| 20 | Amenity | Empty name | ValueError | ValueError | Pass |
| 21 | Amenity | Name > 50 chars | ValueError | ValueError | Pass |

## cURL Testing Examples

### Create a User
```bash
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john@test.com"}'
```

### Create a Review
```bash
curl -X POST http://localhost:5000/api/v1/reviews/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Great", "rating": 5, "user_id": "<USER_ID>", "place_id": "<PLACE_ID>"}'
```

### Get Reviews for a Place
```bash
curl http://localhost:5000/api/v1/places/<PLACE_ID>/reviews
```

### Delete Non-existent Review (Edge Case)
```bash
curl -X DELETE http://localhost:5000/api/v1/reviews/invalid-id
```
Expected: 404 Not Found.

## Edge Cases Covered

- Empty required fields
- String length limits (50, 100 characters)
- Numeric range validation (price, latitude, longitude, rating)
- Non-existent foreign IDs
- Invalid email format
- Duplicate email registration
- Requesting non-existent resources (404)

## Swagger Documentation

API is documented via Flask-RESTx at `http://localhost:5000/api/v1/docs`.
