import uuid

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from transactions_app.models import Transaction
from transactions_app.tests.test_transaction_list_view import transaction
from users_app.models import User


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create(id=uuid.uuid4(), first_name="John", last_name="Doe", email="john@example.com")


@pytest.mark.django_db
def test_export_transactions_csv(api_client, user):
    transaction1 = Transaction.objects.create(amount=100.00, date='2024-01-01', transaction_type='income', category='salary', user=user)
    transaction2 = Transaction.objects.create(amount=50.00, date='2024-01-02', transaction_type='expense', category='food', user=user)

    response = api_client.get(reverse('export-transactions'))
    assert response.status_code == status.HTTP_200_OK
    assert response['Content-Type'] == 'text/csv'
    assert response['Content-Disposition'] == 'attachment; filename="transactions.csv"'

    csv_content = response.content.decode('utf-8').splitlines()
    assert csv_content[0] == 'Id,amount,date,transaction_type,category,user_id'
    assert csv_content[1].split(",")[0] == str(transaction1.id)
    assert csv_content[2].split(",")[0] == str(transaction2.id)
