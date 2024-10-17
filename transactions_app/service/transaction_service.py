import uuid
from abc import ABC, abstractmethod
from typing import List
from transactions_app.models import Transaction


class TransactionService(ABC):
    """
    Abstract class that defines the interface for transaction-related functionality.
    This includes creating, updating, deleting, and retrieving transactions.
    """

    @staticmethod
    @abstractmethod
    def create_transaction(user_id: uuid.UUID, amount: float, transaction_type: str,
                           category: str, date: str) -> Transaction:
        """
        Create and save a new transaction into the database.

        :param user_id: The ID of the user who made the transaction.
        :param amount: The amount of the transaction.
        :param transaction_type: The type of the transaction (e.g., 'income', 'expense').
        :param category: The category of the transaction (e.g., 'salary', 'groceries').
        :param date: The date of the transaction.
        :return: The created and saved Transaction instance.
        """
        pass

    @staticmethod
    @abstractmethod
    def update_transaction(transaction_id: uuid.UUID, **kwargs: dict[str, str]) -> Transaction:
        """
        Update an existing transaction's details in the database.

        :param transaction_id: The ID of the transaction to be updated.
        :param kwargs: A dictionary of fields to update (e.g., amount, category).
        :return: The updated Transaction instance.
        """
        pass

    @staticmethod
    @abstractmethod
    def delete_transaction(transaction_id: uuid.UUID) -> None:
        """
        Delete an existing transaction from the database.

        :param transaction_id: The ID of the transaction to be deleted.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_all_transactions() -> List[Transaction]:
        """
        Retrieve all transactions from the database.

        :return: A list of all Transaction instances.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_transaction_by_id(transaction_id: uuid.UUID) -> Transaction:
        """
        Retrieve a transaction by its unique ID.

        :param transaction_id: The ID of the transaction to retrieve.
        :return: The Transaction instance that matches the given ID.
        """
        pass
