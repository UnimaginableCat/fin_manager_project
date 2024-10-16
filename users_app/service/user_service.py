import uuid
from abc import ABC, abstractmethod
from typing import List

from users_app.models import User


class UserService(ABC):
    """
    Abstract class that defines the interface for user functionality(save user, get user by id, delete user by id).
    """
    @staticmethod
    @abstractmethod
    def save_new_user(first_name: str, last_name: str, email: str) -> User:
        """
        Function that saves a new user into the database
        :param first_name: user first name
        :param last_name:  user last name
        :param email:  user email
        :return: saved user
        """

    pass

    @staticmethod
    @abstractmethod
    def update_existing_user(user_id: uuid.UUID, first_name: str, last_name: str, email: str) -> User:
        """
        Function that updates an existing user
        :param user_id:  id
        :param first_name: user first name
        :param last_name:  user last name
        :param email: user email
        :return: updated user
        """
        pass

    @staticmethod
    @abstractmethod
    def delete_user(user_id: uuid.UUID) -> None:
        """
        Function that deletes an existing user
        :param user_id:
        """

        pass

    @staticmethod
    @abstractmethod
    def get_all_users() -> List[User]:
        """
        Function that returns all users
        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def get_user_by_id(user_id: uuid.UUID) -> User:
        """
        Function that returns user by id
        :param user_id:
        :return: user
        """
        pass
