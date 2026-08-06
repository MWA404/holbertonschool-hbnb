# HBnB Evolution - Part 3

This is Part 3 of the HBnB Evolution project. It adds persistent storage using SQLAlchemy, JWT-based authentication, password hashing with bcrypt, and raw SQL database scripts.

## What's New in Part 3

- Database persistence using SQLAlchemy (replaces in-memory storage from Part 2)
- JWT authentication for protected endpoints
- Password hashing with bcrypt
- Raw SQL scripts for schema creation and initial data
- ER diagram documenting the database structure

## Project Structure

part3/
- app/
  - __init__.py
  - api/v1/ (users.py, auth.py)
  - models/ (base.py, user.py, place.py, review.py, amenity.py)
  - persistence/repository.py
  - services/ (facade.py, repositories/user_repository.py)
- sql/ (schema.sql, initial_data.sql, test_crud.sql, er_diagram.md, README.md)
- config.py
- requirements.txt
- run.py
- README.md

## Installation

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Running the App

python3 run.py

## Setting Up the Raw SQL Database

For MySQL setup independent of SQLAlchemy, use the scripts in sql/:

mysql -uroot -p < sql/schema.sql
mysql -uroot -p < sql/initial_data.sql

See sql/README.md for details.

## Authentication

- POST /api/v1/auth/login - Login with email and password to receive a JWT token
- Include the token in the Authorization: Bearer <token> header for protected routes

## Admin User

- Email: admin@hbnb.io
- Password: admin1234
- is_admin: TRUE
