import uuid
import logging
from typing import List
from transactions_app.models import Transaction
from transactions_app.service.transaction_service import TransactionService
from users_app.service.user_service_impl import UserServiceImpl


class TransactionServiceImpl(TransactionService):
    logger = logging.getLogger(__name__)

    @staticmethod
    def create_transaction(user_id: uuid.UUID, amount: float, transaction_type: str, category: str,
                           date: str) -> Transaction:
        TransactionServiceImpl.logger.info(f"Creating a new transaction for user {user_id}")
        user = UserServiceImpl.get_user_by_id(user_id)

        transaction = Transaction(
            user=user,
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            date=date
        )

        transaction = transaction.save()
        return transaction

    @staticmethod
    def update_transaction(transaction_id: uuid.UUID, **kwargs: dict[str, str]) -> Transaction:
        TransactionServiceImpl.logger.info(f"Updating transaction with id: {transaction_id}")
        transaction = Transaction.objects.get(id=transaction_id)
        for attr, value in kwargs.items():
            if hasattr(transaction, attr):
                setattr(transaction, attr, value)
        transaction = transaction.save()
        return transaction

    @staticmethod
    def delete_transaction(transaction_id: uuid.UUID) -> None:
        TransactionServiceImpl.logger.info(f"Deleting transaction with id: {transaction_id}")
        transaction = Transaction.objects.get(id=transaction_id)
        transaction.delete()

    @staticmethod
    def get_all_transactions() -> List[Transaction]:
        TransactionServiceImpl.logger.info("Retrieving all transactions")
        transactions = Transaction.objects.all()
        return transactions

    @staticmethod
    def get_transaction_by_id(transaction_id: uuid.UUID) -> Transaction:
        TransactionServiceImpl.logger.info(f"Retrieving transaction with id: {transaction_id}")
        transaction = Transaction.objects.get(id=transaction_id)
        return transaction
