import uuid
from decimal import Decimal

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from transactions_app.models import Transaction
from users_app.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create(first_name="John", last_name="Doe", email="john@example.com")


@pytest.fixture
def transaction(user):
    return Transaction.objects.create(
        user=user,
        amount=100.0,
        transaction_type="income",
        category="salary",
        date="2024-01-01"
    )


@pytest.mark.django_db
def test_get_transaction_by_id(api_client, transaction):
    """
    Test case: Retrieve a single transaction by its ID.

    Scenario:
    - Create a transaction in the database.
    - Make a GET request to retrieve the transaction by its ID.

    Expected Result:
    - The response status code is 200 (OK).
    - The amount of the retrieved transaction matches the created transaction.
    """
    url = reverse('transaction-detail', args=[transaction.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert Decimal(response.data['amount']) == transaction.amount


@pytest.mark.django_db
def test_get_transaction_by_id_not_found(api_client):
    """
    Test case: Attempt to retrieve a transaction by a non-existent ID.

    Scenario:
    - Make a GET request to retrieve a transaction using a random UUID that doesn't exist.

    Expected Result:
    - The response status code is 404 (Not Found).
    - The response contains an error message indicating the transaction was not found.
    """
    url = reverse('transaction-detail', args=[uuid.uuid4()])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == 'Transaction not found'


@pytest.mark.django_db
def test_update_transaction(api_client, transaction, user):
    """
    Test case: Update an existing transaction via PUT request with valid data.

    Scenario:
    - Send a PUT request with updated transaction data (user ID, amount, transaction type, category, date).

    Expected Result:
    - The response status code is 200 (OK).
    - The response contains a success message indicating the transaction was updated.
    """
    url = reverse('transaction-detail', args=[transaction.id])

    data = {
        "user": user.id,
        "amount": 150.0,
        "transaction_type": "income",
        "category": "bonus",
        "date": "2024-03-01"
    }
    response = api_client.put(url, data, format='json')
    updated_transaction = Transaction.objects.get(id=transaction.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['detail'] == 'Transaction updated'
    assert updated_transaction.amount == 150.0


@pytest.mark.django_db
def test_update_transaction_not_found(api_client, user):
    """
    Test case: Attempt to update a transaction that does not exist.

    Scenario:
    - Send a PUT request with transaction data to update a non-existent transaction by using a random UUID.

    Expected Result:
    - The response status code is 404 (Not Found).
    - The response contains an error message indicating the transaction was not found.
    """
    url = reverse('transaction-detail', args=[uuid.uuid4()])
    data = {
        "user": user.id,
        "amount": 150.0,
        "transaction_type": "income",
        "category": "bonus",
        "date": "2024-03-01"
    }
    response = api_client.put(url, data, format='json')

    print(response)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == 'Transaction not found'


@pytest.mark.django_db
def test_update_transaction_validation_fail(api_client, transaction, user):
    """
    Test case: Attempt to update a transaction with invalid data.

    Scenario:
    - Send a PUT request with an invalid transaction type.

    Expected Result:
    - The response status code is 400 (Bad Request).
    - The response contains a validation error for the 'transaction_type' field.
    """
    url = reverse('transaction-detail', args=[transaction.id])

    data = {
        "user": user.id,
        "amount": 150.0,
        "transaction_type": "invalid",
        "category": "bonus",
        "date": "2024-03-01"
    }
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "transaction_type" in response.data


@pytest.mark.django_db
def test_delete_transaction(api_client, transaction):
    """
    Test case: Delete an existing transaction via DELETE request.

    Scenario:
    - Create a transaction in the database.
    - Send a DELETE request to remove the transaction.

    Expected Result:
    - The response status code is 204 (No Content).
    """
    url = reverse('transaction-detail', args=[transaction.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_transaction_not_found(api_client):
    """
    Test case: Attempt to delete a transaction that does not exist.

    Scenario:
    - Send a DELETE request to remove a transaction using a random UUID that doesn't exist.

    Expected Result:
    - The response status code is 404 (Not Found).
    - The response contains an error message indicating the transaction was not found.
    """
    url = reverse('transaction-detail', args=[uuid.uuid4()])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == 'Transaction not found'
