import uuid
from decimal import Decimal

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from transactions_app.models import Transaction
from users_app.models import User
from rest_framework import status


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
def test_get_all_transactions(api_client, transaction):
    """
    Test case: Retrieve all transactions via GET request.

    Scenario:
    - Create a transaction in the database.
    - Make a GET request to retrieve the list of transactions.

    Expected Result:
    - The response status code is 200 (OK).
    - The response contains a list of transactions with a length of 1.
    - The amount of the transaction matches the expected value.
    """
    url = reverse('transactions')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert Decimal(response.data[0]['amount']) == 100.0


@pytest.mark.django_db
def test_get_all_transactions_empty(api_client):
    """
    Test case: Retrieve all transactions when none exist.

    Scenario:
    - Make a GET request to retrieve the list of transactions with no transactions in the database.

    Expected Result:
    - The response status code is 200 (OK).
    - The response contains an empty list of transactions.
    """
    url = reverse('transactions')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0


@pytest.mark.django_db
def test_create_transaction(api_client, user):
    """
    Test case: Create a new transaction via POST request with valid data.

    Scenario:
    - Send a POST request with valid transaction data (user ID, amount, transaction type, category, date).

    Expected Result:
    - The response status code is 201 (Created).
    - The response contains a success message indicating the transaction was created.
    """
    url = reverse('transactions')
    data = {
        "user": user.id,
        "amount": 200.0,
        "transaction_type": "expense",
        "category": "groceries",
        "date": "2024-02-01"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['detail'] == "Transaction created"


@pytest.mark.django_db
def test_create_transaction_invalid_amount(api_client, user):
    """
    Test case: Attempt to create a new transaction with a negative amount.

    Scenario:
    - Send a POST request with a negative amount.

    Expected Result:
    - The response status code is 400 (Bad Request).
    - The response contains a validation error for the 'amount' field.
    """
    url = reverse('transactions')
    data = {
        "user": user.id,
        "amount": -200.0,
        "transaction_type": "expense",
        "category": "groceries",
        "date": "2024-02-01"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "amount" in response.data


@pytest.mark.django_db
def test_create_transaction_invalid_user(api_client):
    """
    Test case: Attempt to create a new transaction with an invalid user ID.

    Scenario:
    - Send a POST request with a user ID that does not exist.

    Expected Result:
    - The response status code is 400 (Bad Request).
    - The response contains a validation error for the 'user' field.
    """
    url = reverse('transactions')
    data = {
        "user": uuid.uuid4(),
        "amount": 200.0,
        "transaction_type": "expense",
        "category": "groceries",
        "date": "2024-02-01"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "user" in response.data

@pytest.mark.django_db
def test_create_transaction_invalid_transaction_type(api_client, user):
    """
    Test case: Attempt to create a new transaction with an invalid transaction type.

    Scenario:
    - Send a POST request with an invalid transaction type.

    Expected Result:
    - The response status code is 400 (Bad Request).
    - The response contains a validation error for the 'transaction_type' field.
    """
    url = reverse('transactions')
    data = {
        "user": user.id,
        "amount": 200.0,
        "transaction_type": "hello",
        "category": "groceries",
        "date": "2024-02-01"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "transaction_type" in response.data

@pytest.mark.django_db
def test_create_transaction_invalid_date(api_client, user):
    """
    Test case: Attempt to create a new transaction with an invalid date format.

    Scenario:
    - Send a POST request with an invalid date string.

    Expected Result:
    - The response status code is 400 (Bad Request).
    - The response contains a validation error for the 'date' field.
    """
    url = reverse('transactions')
    data = {
        "user": user.id,
        "amount": 200.0,
        "transaction_type": "expense",
        "category": "groceries",
        "date": "invalid"
    }
    response = api_client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "date" in response.data
