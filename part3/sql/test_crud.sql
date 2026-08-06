-- Test CRUD operations

-- SELECT: verify data was inserted
SELECT * FROM users;
SELECT * FROM amenities;

-- INSERT: add a test user (proper 36-char UUID)
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES ('11111111-2222-3333-4444-555555555555', 'Test', 'User', 'test@hbnb.io', 'testpass', FALSE);

-- UPDATE: modify a user
UPDATE users SET first_name = 'Updated' WHERE email = 'test@hbnb.io';
SELECT * FROM users WHERE email = 'test@hbnb.io';

-- DELETE: remove the test user
DELETE FROM users WHERE email = 'test@hbnb.io';
SELECT * FROM users;

-- Test amenity operations
INSERT INTO amenities (id, name) VALUES ('22222222-3333-4444-5555-666666666666', 'Parking');
SELECT * FROM amenities;
UPDATE amenities SET name = 'Free Parking' WHERE id = '22222222-3333-4444-5555-666666666666';
DELETE FROM amenities WHERE id = '22222222-3333-4444-5555-666666666666';
