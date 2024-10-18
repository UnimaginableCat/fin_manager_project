import datetime
import uuid
from typing import List

from django.db.models import Sum

from reports_app.models import TransactionReport
from reports_app.service.transaction_report_service import TransactionReportService
from transactions_app.models import Transaction


class TransactionReportServiceImpl(TransactionReportService):
    @staticmethod
    def create_report(start_date: datetime.date, end_date: datetime.date) -> TransactionReport:
        transactions = Transaction.objects.filter(date__range=[start_date, end_date])
        total_income = transactions.filter(transaction_type='income').aggregate(Sum('amount'))
        total_expense = transactions.filter(transaction_type='expense').aggregate(Sum('amount'))

        transaction_report = TransactionReport(start_date=start_date,
                                               end_date=end_date,
                                               total_income=total_income['amount__sum'],
                                               total_expense=total_expense['amount__sum'],
                                               net_income=total_income['amount__sum'] - total_expense['amount__sum'])

        transaction_report.save()
        return transaction_report


    @staticmethod
    def get_report_by_id(id: uuid.UUID) -> TransactionReport:
        transaction_report = TransactionReport.objects.get(id=id)
        return transaction_report


    @staticmethod
    def get_all_reports() -> List[TransactionReport]:
        transaction_report_list = TransactionReport.objects.all()
        return transaction_report_list
