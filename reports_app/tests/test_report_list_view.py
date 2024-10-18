import uuid
from datetime import datetime
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest
from unicodedata import category

from reports_app.models import TransactionReport
from transactions_app.models import Transaction
from users_app.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    """Fixture to create a test user."""
    return User.objects.create(id=uuid.uuid4(), first_name="John", last_name="Doe", email="john@example.com")


@pytest.fixture
def report_request():
    return {
        "start_date": datetime(2024, 1, 1).date(),
        "end_date": datetime(2024, 1, 31).date(),
    }


@pytest.mark.django_db
def test_create_report_success(api_client, report_request, user):
    """
    Test case: Successfully create a new transaction report.

    Scenario:
    - Create several transactions in the specified date range.
    - Send a POST request with valid data for start_date and end_date.

    Expected Result:
    - The response status code is 201 (Created).
    - The response contains the report data including total_income, total_expense, and net_income.
    """
    Transaction.objects.create(
        user=user,
        amount=1000,
        transaction_type='income',
        date=datetime(2024, 1, 5).date(),
        category='salary'
    )

    Transaction.objects.create(
        user=user,
        amount=500,
        transaction_type='expense',
        date=datetime(2024, 1, 10).date(),
        category='payment'
    )

    Transaction.objects.create(
        user=user,
        amount=2000,
        transaction_type='income',
        date=datetime(2024, 1, 15).date(),
        category='interest'
    )

    url = reverse("reports")
    response = api_client.post(url, report_request, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Decimal(response.data['total_income']) == 3000.0
    assert Decimal(response.data['total_expense']) == 500.0
    assert Decimal(response.data['net_income']) == 2500.0

@pytest.mark.django_db
def test_create_report_invalid_dates(api_client):
    """
    Test case: Attempt to create a transaction report with invalid dates (end_date before start_date).

    Scenario:
    - Send a POST request with end_date before start_date.

    Expected Result:
    - The response status code is 400 (Bad Request).
    - The response contains a validation error for the 'end_date' field.
    """
    url = reverse("reports")
    invalid_data = {
        "start_date": datetime(2024, 1, 31).date(),
        "end_date": datetime(2024, 1, 1).date(),
    }
    response = api_client.post(url, invalid_data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
