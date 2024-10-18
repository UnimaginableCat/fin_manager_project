import uuid
from datetime import datetime

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from reports_app.models import TransactionReport


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_export_transactions_csv(api_client):
    transaction_report1 = TransactionReport.objects.create(total_income=1500.0,
                                                             total_expense=500.0,
                                                             net_income=1000,
                                                             start_date=datetime(year=2023, month=3, day=1).date(),
                                                             end_date=datetime(year=2023, month=4, day=1).date())

    transaction_report2 = TransactionReport.objects.create(total_income=2500.0,
                                                             total_expense=500.0,
                                                             net_income=2000,
                                                             start_date=datetime(year=2023, month=4, day=1).date(),
                                                             end_date=datetime(year=2023, month=5, day=1).date())


    response = api_client.get(reverse('export-reports'))
    assert response.status_code == status.HTTP_200_OK
    assert response['Content-Type'] == 'text/csv'
    assert response['Content-Disposition'] == 'attachment; filename="reports.csv"'

    csv_content = response.content.decode('utf-8').splitlines()
    assert csv_content[0] == 'id,start_date,end_Date,total_income,total_expense,net_income'
    assert csv_content[1].split(",")[0] == str(transaction_report1.id)
    assert csv_content[2].split(",")[0] == str(transaction_report2.id)
