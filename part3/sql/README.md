# SQL Scripts for HBnB Database

This directory contains raw SQL scripts to generate the HBnB database schema, populate it with initial data, and test CRUD operations.

## Files

- `schema.sql` — Creates all tables (users, places, reviews, amenities, place_amenity) with the required columns, constraints, and foreign keys.
- `initial_data.sql` — Inserts the admin user and three default amenities (WiFi, Swimming Pool, Air Conditioning).
- `test_crud.sql` — Runs sample SELECT, INSERT, UPDATE, and DELETE operations to verify that the schema works correctly.

## How to Run

Run the scripts in this order:

```bash
mysql -uroot -p < schema.sql
mysql -uroot -p < initial_data.sql
mysql -uroot -p < test_crud.sql
```

`schema.sql` must run before `initial_data.sql` because the tables have to exist before data can be inserted.

## Database Structure

- **users** — Application users. `email` is unique.
- **places** — Property listings, each linked to an owner (`user_id`).
- **reviews** — User feedback on places. A user can review each place only once (unique constraint on `user_id` + `place_id`). Rating must be between 1 and 5.
- **amenities** — Available features (e.g., WiFi). `name` is unique.
- **place_amenity** — Junction table linking places and amenities (many-to-many).

## Admin User Credentials

- **Email:** `admin@hbnb.io`
- **Password:** `admin1234` (stored as bcrypt hash)
- **ID:** `36c9050e-ddd3-4c3b-9731-9f487208bbc1`
- **is_admin:** TRUE
