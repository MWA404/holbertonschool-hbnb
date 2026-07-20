# HBnB Evolution - Part 2

Welcome to Part 2 of the HBnB Evolution project. In this part, we bring the design from Part 1 to life by building the API and business logic using Python and Flask.

## What This Part Does

We implemented the first two layers of the application:

- The **Presentation Layer** exposes RESTful API endpoints so clients can interact with the system.
- The **Business Logic Layer** contains the entities (User, Place, Review, Amenity) with their validation rules and relationships.

Data is stored in memory for now. In Part 3, we'll swap that out for a real database, but the code is structured so this change will be easy.

## Getting Started

You'll need Python 3 installed. Set up a virtual environment and install the dependencies:

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

## Running the App

    python3 run.py

Once it's running, the API lives at http://localhost:5000 and you can browse the auto-generated Swagger docs at http://localhost:5000/api/v1/docs.

## API Endpoints

### Users
- POST /api/v1/users/ — Register a new user
- GET /api/v1/users/ — List all users
- GET /api/v1/users/<user_id> — Get one user's details
- PUT /api/v1/users/<user_id> — Update a user

### Places
- POST /api/v1/places/ — Create a place listing
- GET /api/v1/places/ — List all places
- GET /api/v1/places/<place_id> — Get details of a specific place
- PUT /api/v1/places/<place_id> — Update a place

### Reviews
- POST /api/v1/reviews/ — Leave a review
- GET /api/v1/reviews/ — List all reviews
- GET /api/v1/reviews/<review_id> — Get a review
- PUT /api/v1/reviews/<review_id> — Update a review
- DELETE /api/v1/reviews/<review_id> — Delete a review
- GET /api/v1/places/<place_id>/reviews — See all reviews for a place

### Amenities
- POST /api/v1/amenities/ — Add a new amenity
- GET /api/v1/amenities/ — List all amenities
- GET /api/v1/amenities/<amenity_id> — Get amenity details
- PUT /api/v1/amenities/<amenity_id> — Update an amenity

## Testing

Run all the tests with:

    python3 -m unittest discover tests

For a detailed breakdown of every test case and what it verifies, check out tests/TESTING.md.
