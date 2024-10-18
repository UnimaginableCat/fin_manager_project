import datetime
import uuid
from abc import ABC, abstractmethod
from typing import List

from reports_app.models import TransactionReport


class TransactionReportService(ABC):
    """
    Abstract base class for handling transaction report operations.

    This class defines the core methods for creating and retrieving financial reports related to transactions.
    """

    @staticmethod
    @abstractmethod
    def create_report(start_date: datetime.date, end_date: datetime.date) -> TransactionReport:
        """
        Create and generate a financial report summarizing transactions between the given start and end dates.

        :param start_date: The start date for the report period.
        :param end_date: The end date for the report period.
        :return: The generated TransactionReport instance.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_report_by_id(id: uuid.UUID) -> TransactionReport:
        """
        Retrieve a specific financial report by its unique ID.

        :param id: The ID of the report to retrieve.
        :return: The TransactionReport instance that matches the given ID.
        """
        pass

    @staticmethod
    @abstractmethod
    def get_all_reports() -> List[TransactionReport]:
        """
        Retrieve all financial reports from the db.

        :return: A list of all TransactionReport instances.
        """
        pass
