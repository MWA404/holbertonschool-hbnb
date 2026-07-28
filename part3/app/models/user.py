from app.models.base import BaseModel
from app import bcrypt


class User(BaseModel):
    """User model with bcrypt password hashing."""

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password using bcrypt."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    