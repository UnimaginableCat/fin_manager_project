import uuid
from datetime import datetime
from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import pytest

from reports_app.models import TransactionReport


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def transaction_report():
    return TransactionReport.objects.create(
        start_date=datetime(2024, 1, 1).date(),
        end_date=datetime(2024, 1, 31).date(),
        total_income=5000.0,
        total_expense=3000.0,
        net_income=2000.0
    )


@pytest.mark.django_db
def test_get_report_by_id_success(api_client, transaction_report):
    """
    Test case: Successfully retrieve a transaction report by ID.

    Scenario:
    - Send a GET request with a valid report ID.

    Expected Result:
    - The response status code is 200 (OK).
    - The response contains the report data for the given ID.
    """
    url = reverse("report-detail", args=[transaction_report.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert Decimal(response.data['total_income']) == transaction_report.total_income
    assert Decimal(response.data['net_income']) == transaction_report.net_income


@pytest.mark.django_db
def test_get_report_by_id_not_found(api_client):
    """
    Test case: Attempt to retrieve a transaction report with a non-existing ID.

    Scenario:
    - Send a GET request with an invalid report ID.

    Expected Result:
    - The response status code is 404 (Not Found).
    - The response does not contain any data.
    """
    non_existent_id = uuid.uuid4()
    url = reverse("report-detail", args=[non_existent_id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
