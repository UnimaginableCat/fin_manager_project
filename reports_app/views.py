import uuid

from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from reports_app.serializers import ReportRequestSerializer, ReportResponseSerializer
from reports_app.service.transaction_report_service_impl import TransactionReportServiceImpl


class ReportListView(APIView):
    """
    API view to retrieve a list of transaction reports or create a new report.

    GET:
    Retrieve a list of all transaction reports.
    If no reports exist, return an empty list.

    POST:
    Create a new transaction report for a specified date range.
    The report summarizes all transactions (income and expenses) for the given period.
    """

    @swagger_auto_schema(
        operation_description="Create a new transaction report",
        request_body=ReportRequestSerializer,
        responses={
            201: openapi.Response('Report created', ReportResponseSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request: Request) -> Response:
        """
        Handle POST requests to create a new transaction report for a specified date range.

        This method takes the report data from the request (start_date, end_date), validates it using the
        `ReportRequestSerializer`, and if valid, creates a new report through the `TransactionReportServiceImpl`.
        If the data is invalid, it returns the validation errors.
        """
        serializer = ReportRequestSerializer(data=request.data)
        if serializer.is_valid():
            transaction_report = TransactionReportServiceImpl.create_report(
                start_date=serializer.validated_data['start_date'],
                end_date=serializer.validated_data['end_date'])
            response_serializer = ReportResponseSerializer(transaction_report)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Retrieve a list of all transaction reports",
        responses={200: ReportResponseSerializer(many=True)}
    )
    def get(self, request: Request) -> Response:
        """
        Handle GET requests to return a list of all transaction reports.

        This method retrieves all transaction reports from the database via `TransactionReportServiceImpl`,
        serializes them into JSON, and returns the serialized data in the response.
        """
        report_list = TransactionReportServiceImpl.get_all_reports()
        serializer = ReportResponseSerializer(report_list, many=True)
        return Response(serializer.data)


class ReportDetailsView(APIView):
    """
    API view to retrieve a specific transaction report by its ID.

    GET:
    Retrieve the details of a transaction report by its ID.
    If the report is not found, return a 404 error.
    """
    @swagger_auto_schema(
        operation_description="Retrieve a transaction report by ID",
        responses={
            200: ReportResponseSerializer(),
            404: openapi.Response('Report not found')
        }
    )
    def get(self, request: Request, id: uuid.UUID) -> Response:
        """
        Handle GET requests to retrieve a transaction report by ID.

        This method retrieves the transaction report via `TransactionReportServiceImpl`, serializes it into JSON,
        and returns the serialized data in the response. If the report is not found, a 404 error is returned.
        """
        try:
            transaction_report = TransactionReportServiceImpl.get_report_by_id(id)
            response_serializer = ReportResponseSerializer(transaction_report)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
