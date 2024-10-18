import uuid
from datetime import datetime
from unittest import mock

import pytest
from unittest.mock import MagicMock
from django.core.exceptions import ObjectDoesNotExist

from reports_app.models import TransactionReport
from reports_app.service.transaction_report_service_impl import TransactionReportServiceImpl
from transactions_app.models import Transaction


@pytest.fixture
def transaction_report_entity():
    return TransactionReport(
        id=uuid.uuid4(),
        start_date=datetime(2024, 1, 1).date(),
        end_date=datetime(2024, 1, 31).date(),
        total_income=5000,
        total_expense=3000,
        net_income=2000
    )


@pytest.fixture
def transaction_data():
    return {
        "start_date": datetime(2024, 1, 1).date(),
        "end_date": datetime(2024, 1, 31).date(),
    }


@pytest.fixture
def transactions_mock():
    return [
        Transaction(id=uuid.uuid4(), transaction_type='income', amount=5000),
        Transaction(id=uuid.uuid4(), transaction_type='expense', amount=3000)
    ]


@mock.patch.object(TransactionReport, "save")
@mock.patch.object(Transaction, "objects")
def test_create_report(mock_transaction_objects: MagicMock,
                       mock_report_save: MagicMock,
                       transaction_data,
                       transaction_report_entity):
    """Test creating a transaction report successfully.

    This test mocks the Transaction model's filter and aggregate methods, as well as
    the TransactionReport's save method, to ensure the report is created correctly.
    """
    mock_transaction_objects.filter.return_value.filter.return_value.aggregate.side_effect = [
        {'amount__sum': 5000},  # total_income
        {'amount__sum': 3000}   # total_expense
    ]

    report = TransactionReportServiceImpl.create_report(
        start_date=transaction_data["start_date"],
        end_date=transaction_data["end_date"]
    )

    mock_report_save.assert_called_once()
    assert report.total_income == 5000
    assert report.total_expense == 3000
    assert report.net_income == 2000


@mock.patch.object(TransactionReport, "objects")
def test_get_report_by_id(mock_report_objects: MagicMock, transaction_report_entity):
    """Test retrieving a transaction report by its ID successfully.

    This test checks that the get_report_by_id method retrieves the correct report
    for a given UUID.
    """
    mock_report_objects.get.return_value = transaction_report_entity

    report = TransactionReportServiceImpl.get_report_by_id(transaction_report_entity.id)

    mock_report_objects.get.assert_called_once_with(id=transaction_report_entity.id)
    assert report == transaction_report_entity


@mock.patch.object(TransactionReport, "objects")
def test_get_report_by_id_not_found(mock_report_objects: MagicMock):
    """Test retrieving a report by ID fails when the report is not found.

    This test checks that attempting to retrieve a non-existing report raises
    an ObjectDoesNotExist exception.
    """
    mock_report_objects.get.side_effect = ObjectDoesNotExist("Not Found")

    with pytest.raises(ObjectDoesNotExist):
        TransactionReportServiceImpl.get_report_by_id(uuid.uuid4())

    mock_report_objects.get.assert_called_once()


@mock.patch.object(TransactionReport, "objects")
def test_get_all_reports(mock_report_objects: MagicMock, transaction_report_entity):
    """Test retrieving all transaction reports.

    This test mocks the all method of the TransactionReport model and asserts that
    it returns the correct number of reports.
    """
    mock_report_objects.all.return_value = [transaction_report_entity]

    reports = TransactionReportServiceImpl.get_all_reports()

    mock_report_objects.all.assert_called_once()
    assert len(reports) == 1
    assert reports[0] == transaction_report_entity
