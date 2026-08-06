-- Initial data for HBnB

INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$X8ok8pv06BpV0zZbEnvXPO9lYyBWjKevVeqcuoI2Sk7whWXQBFCsu',
    TRUE
);

INSERT INTO amenities (id, name) VALUES
    ('a1b2c3d4-1111-2222-3333-444455556666', 'WiFi'),
    ('a1b2c3d4-1111-2222-3333-444455557777', 'Swimming Pool'),
    ('a1b2c3d4-1111-2222-3333-444455558888', 'Air Conditioning');
