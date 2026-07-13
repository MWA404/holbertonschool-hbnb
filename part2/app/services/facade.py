import re

from app.models.user import User
from app.persistence.repository import InMemoryRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()

    @staticmethod
    def _validate_user_data(user_data):
        """Validate user payload (models have no validation of their own)."""
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        email = user_data.get('email')

        if not first_name or not isinstance(first_name, str) \
                or len(first_name) > 50:
            raise ValueError("first_name is required (max 50 characters)")
        if not last_name or not isinstance(last_name, str) \
                or len(last_name) > 50:
            raise ValueError("last_name is required (max 50 characters)")
        if not email or not isinstance(email, str) \
                or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            raise ValueError("A valid email is required")

    def create_user(self, user_data):
        self._validate_user_data(user_data)
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        # The repository has no get_by_attribute, so we scan get_all()
        return next(
            (u for u in self.user_repo.get_all() if u.email == email),
            None
        )

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
        self._validate_user_data(user_data)
        return self.user_repo.update(user_id, user_data)
