-- Test CRUD operations

-- SELECT: verify data was inserted
SELECT * FROM users;
SELECT * FROM amenities;

-- INSERT: add a test user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES ('test-1234-5678-9012-345678901234', 'Test', 'User', 'test@hbnb.io', 'testpass', FALSE);

-- UPDATE: modify a user
UPDATE users SET first_name = 'Updated' WHERE email = 'test@hbnb.io';
SELECT * FROM users WHERE email = 'test@hbnb.io';

-- DELETE: remove the test user
DELETE FROM users WHERE email = 'test@hbnb.io';
SELECT * FROM users;
