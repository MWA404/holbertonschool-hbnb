from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Repository for user-specific database operations."""

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.model.query.filter_by(email=email).first()
