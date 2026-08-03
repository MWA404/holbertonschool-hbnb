from app.models.base import BaseModel
from app import bcrypt, db


class User(BaseModel):
    """User model with bcrypt password hashing."""

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(
        db.String(120),
        nullable=False,
        unique=True
    )
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship(
        'Place',
        backref='owner',
        lazy=True
    )

    reviews = db.relationship(
        'Review',
        backref='user',
        lazy=True
    )

    def __init__(
        self,
        first_name,
        last_name,
        email,
        password=None,
        is_admin=False
    ):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        if password:
            self.hash_password(password)

    def hash_password(self, password):
        """Hashes the password using bcrypt."""
        self.password = bcrypt.generate_password_hash(
            password
        ).decode('utf-8')

    def verify_password(self, password):
        """Verifies the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
