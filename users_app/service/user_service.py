import uuid
from abc import ABC, abstractmethod
from typing import List

from users_app.models import User


class UserService(ABC):
    """
    Abstract class that defines the interface for user-related functionality.
    This includes creating, updating, deleting, and retrieving users.
    """

    @staticmethod
    @abstractmethod
    def save_new_user(first_name: str, last_name: str, email: str) -> User:
        """
        Create and save a new user into the database.

        :param first_name: The first name of the user.
        :param last_name: The last name of the user.
        :param email: The email address of the user.
        :return: The created and saved User instance.
        """
        pass

    @staticmethod
    @abstractmethod
    def update_existing_user(user_id: uuid.UUID, **kwargs: dict[str, str]) -> User:
        """
        Update an existing user's details in the database.

        :param user_id: The ID of the user to be updated.
        :param kwargs: A dictionary of fields to update (e.g., first_name, last_name).
        :return: The updated User instance.
        """
        pass

    @staticmethod
    @abstractmethod
    def delete_user(user_id: uuid.UUID) -> None:
        """
        Delete an existing user from the database.

        :param user_id: The ID of the user to be deleted.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_all_users() -> List[User]:
        """
        Retrieve all users from the database.

        :return: A list of all User instances.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_user_by_id(user_id: uuid.UUID) -> User:
        """
        Retrieve a user by their unique ID.

        :param user_id: The ID of the user to retrieve.
        :return: The User instance that matches the given ID.
        """
        pass
