import uuid
from unittest import mock
import pytest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist
from transactions_app.models import Transaction
from transactions_app.service.transaction_service_impl import TransactionServiceImpl
from users_app.models import User
from users_app.service.user_service_impl import UserServiceImpl


@pytest.fixture
def request_data():
    return {
        "user_id": uuid.uuid4(),
        "amount": 100.0,
        "transaction_type": "income",
        "category": "salary",
        "date": "2024-01-01"
    }


@pytest.fixture
def transaction_entity() -> Transaction:
    return Transaction(
        id=uuid.uuid4(),
        # user_id=uuid.uuid4(),
        amount=100.0,
        transaction_type="income",
        category="salary",
        date="2024-01-01"
    )


@pytest.fixture
def user_entity() -> User:
    return User(
        id=uuid.uuid4(),
        first_name="John",
        last_name="Doe",
        email="doe@mail.com",
        reg_date="2022-01-01"
    )


@mock.patch.object(UserServiceImpl, "get_user_by_id")
@mock.patch.object(Transaction, "save")
def test_create_transaction(mock_transaction_save: MagicMock,
                            mock_user_service: MagicMock,
                            user_entity,
                            request_data,
                            transaction_entity):
    """Test creating a new transaction successfully.

    This test mocks the save method of the Transaction model and asserts that
    the method is called once when saving a new transaction.
    """
    transaction_entity.user_id = request_data['user_id']
    mock_user_service.return_value = user_entity
    result = TransactionServiceImpl.create_transaction(**request_data)
    mock_transaction_save.assert_called_once()
    assert result.amount == request_data['amount']


@mock.patch.object(UserServiceImpl, "get_user_by_id")
@mock.patch.object(Transaction, "save")
def test_create_transaction_fail(mock_transaction_save: MagicMock, mock_user_service: MagicMock, request_data,
                                 user_entity):
    """Test creating a new transaction fails due to a database error.

    This test mocks the save method to raise an exception and checks
    that the exception is correctly raised.
    """
    mock_user_service.return_value = user_entity
    mock_transaction_save.side_effect = Exception("Database error")
    with pytest.raises(Exception, match="Database error"):
        TransactionServiceImpl.create_transaction(**request_data)
    mock_transaction_save.assert_called_once()


@mock.patch.object(Transaction, "save")
@mock.patch.object(Transaction, "objects")
def test_update_transaction(mock_transaction_objects: MagicMock,
                            mock_transaction_save: MagicMock,
                            request_data,
                            transaction_entity):
    """Test updating an existing transaction successfully.

    This test checks that the update_transaction method calls the
    get method and save method of the Transaction model correctly, and asserts
    that the returned transaction has the updated amount.
    """
    updated_amount = 200.0
    transaction_id = transaction_entity.id
    transaction_entity.user_id = request_data['user_id']

    mock_transaction_objects.get.return_value = transaction_entity

    result = TransactionServiceImpl.update_transaction(transaction_id, amount=updated_amount)

    mock_transaction_objects.get.assert_called_once_with(id=transaction_id)
    mock_transaction_save.assert_called_once()

    assert result.amount == updated_amount


@mock.patch.object(Transaction, "objects")
def test_update_transaction_not_found(mock_transaction_objects: MagicMock, transaction_entity):
    """Test updating an existing transaction fails when transaction is not found.

    This test checks that attempting to update a transaction that does not exist
    raises an ObjectDoesNotExist exception.
    """
    mock_transaction_objects.get.side_effect = ObjectDoesNotExist("Not Found")

    with pytest.raises(ObjectDoesNotExist):
        TransactionServiceImpl.update_transaction(transaction_entity.id, amount=200.0)

    mock_transaction_objects.get.assert_called_once_with(id=transaction_entity.id)


@mock.patch.object(Transaction, "delete")
@mock.patch.object(Transaction, "objects")
def test_delete_transaction(mock_transaction_objects: MagicMock, mock_transaction_delete: MagicMock,
                            transaction_entity):
    """Test deleting an existing transaction successfully.

    This test verifies that the delete_transaction method correctly calls the
    delete method of the Transaction model for the given transaction.
    """
    mock_transaction_objects.get.return_value = transaction_entity

    TransactionServiceImpl.delete_transaction(transaction_entity.id)
    mock_transaction_delete.assert_called_once()


@mock.patch.object(Transaction, "delete")
@mock.patch.object(Transaction, "objects")
def test_delete_transaction_not_found(mock_transaction_objects: MagicMock, mock_transaction_delete: MagicMock,
                                      transaction_entity):
    """Test deleting a transaction fails when transaction is not found.

    This test checks that attempting to delete a transaction that does not exist
    raises an ObjectDoesNotExist exception.
    """
    mock_transaction_objects.get.side_effect = ObjectDoesNotExist("Not Found")

    with pytest.raises(ObjectDoesNotExist):
        TransactionServiceImpl.delete_transaction(transaction_entity.id)

    mock_transaction_objects.get.assert_called_once_with(id=transaction_entity.id)
    mock_transaction_delete.assert_not_called()


@mock.patch.object(Transaction, "objects")
def test_get_all_transactions(mock_transaction_objects: MagicMock, transaction_entity):
    """Test retrieving all transactions.

    This test mocks the all method of the Transaction model and asserts that
    it returns the correct number of transactions.
    """
    mock_transaction_objects.all.return_value = [transaction_entity]
    result = TransactionServiceImpl.get_all_transactions()
    mock_transaction_objects.all.assert_called_once()
    assert len(result) == len(mock_transaction_objects.all.return_value)


@mock.patch.object(Transaction, "objects")
def test_get_transaction_by_id(mock_transaction_objects: MagicMock, transaction_entity):
    """Test retrieving a transaction by ID successfully.

    This test checks that the get_transaction_by_id method correctly retrieves
    the transaction for the given ID.
    """
    mock_transaction_objects.get.return_value = transaction_entity
    result = TransactionServiceImpl.get_transaction_by_id(transaction_entity.id)

    mock_transaction_objects.get.assert_called_once_with(id=transaction_entity.id)
    assert result == transaction_entity


@mock.patch.object(Transaction, "objects")
def test_get_transaction_by_id_not_found(mock_transaction_objects: MagicMock, transaction_entity):
    """Test retrieving a transaction by ID fails when transaction is not found.

    This test checks that attempting to retrieve a transaction that does not exist
    raises an ObjectDoesNotExist exception.
    """
    mock_transaction_objects.get.side_effect = ObjectDoesNotExist("Not Found")
    with pytest.raises(ObjectDoesNotExist):
        TransactionServiceImpl.get_transaction_by_id(transaction_entity.id)

    mock_transaction_objects.get.assert_called_once_with(id=transaction_entity.id)
