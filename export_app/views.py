import csv
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.views import APIView

from reports_app.service.transaction_report_service_impl import TransactionReportServiceImpl
from transactions_app.service.transaction_service_impl import TransactionServiceImpl


class ExportTransactionsCSVView(APIView):
    """
    API view for exporting all transactions in CSV format.

    GET:
    Returns a CSV file with all transaction data.
    """

    @swagger_auto_schema(
        operation_description="Export all transactions as a CSV file",
        responses={
            200: openapi.Response('CSV file with all transaction data')
        }
    )
    def get(self, request: Request) -> HttpResponse:
        """
        Handle GET requests to export all transactions in CSV format.

        This method retrieves all transactions from the database using `TransactionServiceImpl`
        and returns them as a downloadable CSV file. The CSV includes transaction details such as ID,
        amount, date, transaction type, category, and user ID.
        """
        transactions = TransactionServiceImpl.get_all_transactions()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'

        writer = csv.writer(response)
        writer.writerow(['Id', 'amount', 'date', 'transaction_type', 'category', 'user_id'])
        for transaction in transactions:
            writer.writerow([transaction.id,
                             transaction.amount,
                             transaction.date,
                             transaction.transaction_type,
                             transaction.category,
                             transaction.user.id,
                             ])

        return response


class ExportReportsCSVView(APIView):
    """
    API view for exporting all reports in CSV format.

    GET:
    Returns a CSV file with all report data.
    """

    @swagger_auto_schema(
        operation_description="Export all reports as a CSV file",
        responses={
            200: openapi.Response('CSV file with all report data')
        }
    )
    def get(self, request: Request) -> HttpResponse:
        """
        Handle GET requests to export all reports in CSV format.

        This method retrieves all transaction reports from the database using `TransactionReportServiceImpl`
        and returns them as a downloadable CSV file. The CSV includes report details such as ID,
        start date, end date, total income, total expense, and net income.
        """
        reports = TransactionReportServiceImpl.get_all_reports()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reports.csv"'

        writer = csv.writer(response)
        writer.writerow(['id', 'start_date', 'end_Date', 'total_income', 'total_expense', 'net_income'])
        for report in reports:
            writer.writerow([report.id, report.start_date, report.end_date, report.total_income, report.total_expense,
                             report.net_income])

        return response
