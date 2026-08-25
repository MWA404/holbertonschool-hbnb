# HBnB Evolution

A simplified AirBnB-like web application that lets users register, list properties, manage amenities, and leave reviews.

The project is built in four incremental parts — from UML design, to a Flask REST API, to a database-backed and authenticated backend, and finally to a working web client. Each part builds directly on the one before it.

---

## Table of Contents

- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [The Four Parts](#the-four-parts)
- [Data Model](#data-model)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Authentication](#authentication)
- [Database Setup](#database-setup)
- [Running the Web Client](#running-the-web-client)
- [Testing](#testing)
- [Authors](#authors)

---

## Architecture

The application follows a **three-layer architecture**, with the layers communicating through the **Facade pattern**:

```
┌─────────────────────────────────────┐
│      Presentation Layer             │
│  (REST API — Users, Places,         │
│   Reviews, Amenities endpoints)     │
└──────────────┬──────────────────────┘
               │  Facade Pattern
┌──────────────▼──────────────────────┐
│      Business Logic Layer           │
│  (User, Place, Review, Amenity      │
│   models + validation rules)        │
└──────────────┬──────────────────────┘
               │  Repository Pattern
┌──────────────▼──────────────────────┐
│      Persistence Layer              │
│  (In-memory → SQLAlchemy ORM)       │
└─────────────────────────────────────┘
```

**Why this structure:**

- **Separation of concerns** — each layer has one job, so a change in one rarely breaks the others.
- **Swappable persistence** — Part 2 stores data in memory; Part 3 swaps in SQLAlchemy without rewriting the business logic.
- **Facade pattern** — the API talks to a single simplified interface instead of reaching into every model directly, keeping endpoints thin and readable.

---

## Project Structure

```
holbertonschool-hbnb/
├── part1/                          # UML design & documentation
│   ├── README.md                   # High-level package diagram
│   ├── task1_class_diagram.md      # Class diagram
│   ├── task2_sequence_diagrams.md  # Sequence diagrams
│   └── document.md                 # Compiled technical document
│
├── part2/                          # Flask REST API (in-memory storage)
│   ├── app/
│   │   ├── api/v1/                 # users.py, places.py, reviews.py, amenities.py
│   │   ├── models/                 # base.py, user.py, place.py, review.py, amenity.py
│   │   ├── persistence/            # repository.py (in-memory)
│   │   └── services/               # facade.py
│   ├── tests/                      # test_models.py, test_reviews.py, TESTING.md
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
│
├── part3/                          # Database + authentication
│   ├── app/
│   │   ├── api/v1/                 # + auth.py (login endpoint)
│   │   ├── models/                 # SQLAlchemy-mapped models
│   │   ├── persistence/
│   │   └── services/repositories/  # user_repository.py
│   ├── sql/                        # Raw SQL scripts
│   │   ├── schema.sql              # Table definitions
│   │   ├── initial_data.sql        # Admin user + default amenities
│   │   ├── test_crud.sql           # CRUD verification queries
│   │   ├── er_diagram.md           # Entity-relationship diagram
│   │   └── README.md
│   ├── config.py
│   ├── requirements.txt
│   └── run.py
│
└── part4/                          # Web client (front-end)
    ├── index.html                  # Places listing + price filter
    ├── place.html                  # Place details + reviews
    ├── login.html                  # Login form
    ├── add_review.html             # Review submission form
    ├── scripts.js                  # All client-side logic
    ├── styles.css
    └── images/                     # Amenity icons & logo
```

---

## The Four Parts

### Part 1 — Technical Documentation

The design phase. Produces the blueprint the rest of the project is built from:

- **Package diagram** — the three-layer architecture and how the layers interact
- **Class diagram** — entities (`BaseModel`, `User`, `Place`, `Review`, `Amenity`), their attributes, methods, and relationships
- **Sequence diagrams** — step-by-step request flows for key operations (user registration, place creation, review submission, fetching places)

### Part 2 — Business Logic & API

Brings the design to life with Flask and Flask-RESTx:

- RESTful endpoints for all four entities
- Business-logic models with validation rules
- In-memory repository (deliberately simple — replaced in Part 3)
- Auto-generated Swagger documentation
- Unit tests for models and review logic

### Part 3 — Authentication & Database

Makes the application persistent and secure:

- **SQLAlchemy ORM** replaces in-memory storage
- **JWT authentication** — login issues a signed token used for protected routes
- **bcrypt password hashing** — passwords are never stored in plain text
- **Raw SQL scripts** for schema creation and seeding, independent of the ORM
- **ER diagram** documenting the final database structure

### Part 4 — Simple Web Client

A vanilla HTML/CSS/JavaScript front-end that consumes the API:

- **Login page** — authenticates and stores the JWT in a cookie
- **Index page** — fetches and renders all places, with a client-side price filter
- **Place details** — shows the host, price, description, amenities (with icons), and reviews
- **Add review** — submits a review with the token attached; redirects unauthenticated users

No frameworks are used — everything is done with the Fetch API and DOM manipulation.

---

## Data Model

### Entities

All entities inherit from `BaseModel`, which provides `id` (UUID4), `created_at`, and `updated_at`.

| Entity | Key Attributes |
|---|---|
| **User** | `first_name`, `last_name`, `email` (unique), `password` (hashed), `is_admin` |
| **Place** | `title`, `description`, `price`, `latitude`, `longitude`, `owner_id` |
| **Review** | `text`, `rating` (1–5), `user_id`, `place_id` |
| **Amenity** | `name` (unique), `description` |

### Relationships

| Relationship | Type | Notes |
|---|---|---|
| User → Places | One-to-Many | A user owns many places |
| User → Reviews | One-to-Many | A user writes many reviews |
| Place → Reviews | One-to-Many | A place receives many reviews |
| Place ↔ Amenities | Many-to-Many | Via the `place_amenity` junction table |

### Constraints

- `users.email` is **unique**
- `amenities.name` is **unique**
- `reviews` has a **unique constraint on (`user_id`, `place_id`)** — a user can review each place only once
- `reviews.rating` must be between **1 and 5**
- Foreign keys enforce referential integrity across `places`, `reviews`, and `place_amenity`

---

## Tech Stack

**Backend**
- Python 3
- Flask — web framework
- Flask-RESTx — REST API structure and Swagger docs
- SQLAlchemy / Flask-SQLAlchemy — ORM
- Flask-JWT-Extended — token-based authentication
- Flask-Bcrypt — password hashing
- Flask-CORS — cross-origin request handling

**Frontend**
- HTML5, CSS3
- Vanilla JavaScript (Fetch API, no frameworks)

**Database**
- SQLite (development)
- MySQL (raw SQL scripts)

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- MySQL (optional — only for the raw SQL scripts)

### Installation

Clone the repository:

```bash
git clone https://github.com/MWA404/holbertonschool-hbnb.git
cd holbertonschool-hbnb
```

Set up a virtual environment and install dependencies for the part you want to run:

```bash
cd part3            # or part2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the API

```bash
python3 run.py
```

| Part | Port | Swagger Docs |
|---|---|---|
| Part 2 | `5000` | `http://localhost:5000/api/v1/docs` |
| Part 3 | `5005` | `http://localhost:5005/api/v1/docs` |

> **Note for macOS users:** port 5000 is used by the AirPlay Receiver. If Part 2 fails to start, disable AirPlay Receiver in System Settings or change the port in `run.py`.

---

## API Reference

Base URL: `/api/v1`

### Users

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/users/` | Register a new user |
| `GET` | `/users/` | List all users |
| `GET` | `/users/<user_id>` | Get a single user |
| `PUT` | `/users/<user_id>` | Update a user |

### Places

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/places/` | Create a place listing |
| `GET` | `/places/` | List all places |
| `GET` | `/places/<place_id>` | Get place details |
| `PUT` | `/places/<place_id>` | Update a place |

### Reviews

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/reviews/` | Submit a review |
| `GET` | `/reviews/` | List all reviews |
| `GET` | `/reviews/<review_id>` | Get a review |
| `PUT` | `/reviews/<review_id>` | Update a review |
| `DELETE` | `/reviews/<review_id>` | Delete a review |
| `GET` | `/places/<place_id>/reviews` | List all reviews for a place |

### Amenities

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/amenities/` | Add an amenity |
| `GET` | `/amenities/` | List all amenities |
| `GET` | `/amenities/<amenity_id>` | Get an amenity |
| `PUT` | `/amenities/<amenity_id>` | Update an amenity |

### Status Codes

| Code | Meaning |
|---|---|
| `200` | Success |
| `201` | Resource created |
| `400` | Bad request / validation error |
| `401` | Missing or invalid credentials |
| `403` | Authenticated but not authorized |
| `404` | Resource not found |
| `409` | Conflict (e.g. duplicate email) |

---

## Authentication

Authentication is handled with **JWT (JSON Web Tokens)**.

### Logging In

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin@hbnb.io",
  "password": "admin1234"
}
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

### Using the Token

Attach the token to any protected request:

```http
Authorization: Bearer <access_token>
```

### How It Works

1. The user submits their email and password.
2. The server looks up the user and verifies the password against the stored **bcrypt hash**.
3. On success, it signs a JWT containing the user's ID (`sub` claim) and an expiry.
4. The client stores the token and sends it with subsequent requests.
5. The server decodes the token to identify the user — no server-side session storage needed.

> **Security note:** passwords are hashed with bcrypt, which is one-way. The original password can never be recovered from the stored hash.

### Default Admin Account

| Field | Value |
|---|---|
| Email | `admin@hbnb.io` |
| Password | `admin1234` |
| `is_admin` | `TRUE` |

---

## Database Setup

Part 3 uses **SQLite** by default (created automatically on first run). To use the raw **MySQL** scripts instead:

```bash
cd part3/sql
mysql -uroot -p < schema.sql          # Create tables
mysql -uroot -p < initial_data.sql    # Seed admin user + amenities
mysql -uroot -p < test_crud.sql       # Verify with sample CRUD operations
```

Run them in that order — the tables must exist before data can be inserted.

**Tables created:** `users`, `places`, `reviews`, `amenities`, `place_amenity`

**Seeded data:** the admin user and three default amenities (WiFi, Swimming Pool, Air Conditioning).

---

## Running the Web Client

Start the Part 3 API first, then open the front-end:

```bash
# Terminal 1 — start the API
cd part3
python3 run.py

# Terminal 2 — serve the front-end
cd part4
python3 -m http.server 8000
```

Then visit `http://localhost:8000` in your browser.

> **Why serve it instead of opening the file directly?** Opening `index.html` from the filesystem gives it a `file://` origin, which browsers block from making API requests. Serving it over HTTP avoids this.

### Front-End Flow

1. **Login** (`login.html`) → posts credentials, stores the returned JWT in a cookie, redirects to the index.
2. **Index** (`index.html`) → fetches all places and renders them as cards. The price filter shows and hides cards client-side using each card's `data-price` attribute.
3. **Place details** (`place.html?id=<place_id>`) → reads the place ID from the URL query string, fetches that place, and renders the host, price, description, amenities (with icons), and reviews.
4. **Add review** (`add_review.html?id=<place_id>`) → checks for a token first and redirects unauthenticated visitors; otherwise submits the review with the token attached.

---

## Testing

Run the Part 2 test suite:

```bash
cd part2
python3 -m unittest discover tests
```

See `part2/tests/TESTING.md` for a breakdown of every test case and what it verifies.

You can also test endpoints interactively through the **Swagger UI** at `/api/v1/docs` while the server is running.

For the database layer, `part3/sql/test_crud.sql` runs sample SELECT, INSERT, UPDATE, and DELETE operations to confirm the schema and its constraints behave correctly.

---

## Authors

| Member | Contribution |
|---|---|
| **Muhannad Alraddadi** | System design (UML), database schema and ER diagram, review endpoints, and the web client |
| **Abdulrhman Asiri** | REST API endpoints and SQLAlchemy database integration |
| **Faisal Alshahrani** | Core business logic models and the authentication system (JWT + bcrypt) |

---

## Acknowledgements

Built as part of the **Holberton School** software engineering curriculum.
