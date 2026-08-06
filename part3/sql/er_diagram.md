# HBnB Database ER Diagram

This document contains the Entity-Relationship diagram for the HBnB database schema.

## Diagram

```mermaid
erDiagram
    USERS {
        CHAR(36) id PK
        VARCHAR(255) first_name
        VARCHAR(255) last_name
        VARCHAR(255) email UK
        VARCHAR(255) password
        BOOLEAN is_admin
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    PLACES {
        CHAR(36) id PK
        VARCHAR(255) title
        TEXT description
        DECIMAL price
        FLOAT latitude
        FLOAT longitude
        CHAR(36) user_id FK
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    REVIEWS {
        CHAR(36) id PK
        TEXT text
        INT rating
        CHAR(36) user_id FK
        CHAR(36) place_id FK
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    AMENITIES {
        CHAR(36) id PK
        VARCHAR(255) name UK
        TIMESTAMP created_at
        TIMESTAMP updated_at
    }

    PLACE_AMENITY {
        CHAR(36) place_id PK,FK
        CHAR(36) amenity_id PK,FK
    }

    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"
    PLACES ||--o{ PLACE_AMENITY : "linked to"
    AMENITIES ||--o{ PLACE_AMENITY : "belongs to"
```

## Entity Descriptions

### USERS
Stores application user accounts.
- `id` — Primary key (UUID, 36 characters)
- `email` — Unique identifier used for login
- `password` — Stored as bcrypt hash
- `is_admin` — Boolean flag for administrator privileges

### PLACES
Property listings created by users.
- `user_id` — Foreign key linking to the owner in USERS
- `price` — DECIMAL(10, 2) for currency accuracy

### REVIEWS
User feedback on places.
- `user_id` — Foreign key to the reviewer
- `place_id` — Foreign key to the reviewed place
- `rating` — Integer between 1 and 5 (CHECK constraint)
- Composite unique constraint on (user_id, place_id): a user can only review each place once

### AMENITIES
Available features (WiFi, Pool, etc.).
- `name` — Unique across all amenities

### PLACE_AMENITY
Junction table implementing the many-to-many relationship between places and amenities.
- Composite primary key: (place_id, amenity_id)
- Both columns are also foreign keys

## Relationships

| Relationship | Type | Description |
|---|---|---|
| USERS → PLACES | One-to-Many | One user can own many places |
| USERS → REVIEWS | One-to-Many | One user can write many reviews |
| PLACES → REVIEWS | One-to-Many | One place can have many reviews |
| PLACES ↔ AMENITIES | Many-to-Many | Implemented via PLACE_AMENITY junction table |

## Legend

- **PK** — Primary Key
- **FK** — Foreign Key
- **UK** — Unique Key
