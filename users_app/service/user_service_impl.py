import uuid
import logging
from typing import List

from users_app.models import User
from users_app.service.user_service import UserService


class UserServiceImpl(UserService):
    logger = logging.getLogger(__name__)

    @staticmethod
    def save_new_user(first_name: str, last_name: str, email: str) -> User:
        UserServiceImpl.logger.info(f"Saving new user with email: {email}")
        user = User(first_name=first_name, last_name=last_name, email=email)
        user.save()
        return user

    @staticmethod
    def update_existing_user(user_id: uuid.UUID, **kwargs: dict[str, str]) -> User:
        UserServiceImpl.logger.info(f"Updating user with id: {user_id}")
        user = User.objects.get(id=user_id)
        for attr, value in kwargs.items():
            if hasattr(user, attr):
                setattr(user, attr, value)
        user.save()
        return user

    @staticmethod
    def delete_user(user_id: uuid.UUID) -> None:
        UserServiceImpl.logger.info(f"Deleting user with id: {user_id}")
        user = User.objects.get(id=user_id)
        user.delete()

    @staticmethod
    def get_all_users() -> List[User]:
        UserServiceImpl.logger.info("Getting all users")
        user_list = User.objects.all()
        return user_list

    @staticmethod
    def get_user_by_id(user_id: uuid.UUID) -> User:
        UserServiceImpl.logger.info(f"Getting user with id: {user_id}")
        user = User.objects.get(id=user_id)
        return user
