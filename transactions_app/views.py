import uuid

from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from transactions_app.serializers import TransactionSerializer
from transactions_app.service.transaction_service_impl import TransactionServiceImpl


class TransactionListView(APIView):
    """
    API view to retrieve list of transactions or create a new transaction.

    GET:
    Return the list of all transactions.
    If no transactions exist, return an empty list.

    POST:
    Create a new transaction based on the provided data.
    Data should include the amount, type (income/expense), category, and date.
    """

    @swagger_auto_schema(
        operation_description="Retrieve a list of all transactions",
        responses={200: TransactionSerializer(many=True)}
    )
    def get(self, request: Request) -> Response:
        """
        Handle GET requests to return a list of all transactions.

        This method retrieves all transactions from the database via the `TransactionServiceImpl`,
        serializes them into JSON, and returns the serialized data in the response.
        """
        transactions = TransactionServiceImpl.get_all_transactions()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new transaction",
        request_body=TransactionSerializer,
        responses={
            201: openapi.Response('Transaction created', TransactionSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request: Request) -> Response:
        """
        Handle POST requests to create a new transaction.

        This method takes the transaction data from the request, validates it using the `TransactionSerializer`,
        and if valid, creates a new transaction through the `TransactionServiceImpl`. If the data is invalid,
        it returns the validation errors.
        """
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            TransactionServiceImpl.create_transaction(
                user_id=serializer.validated_data['user'].id,
                amount=serializer.validated_data['amount'],
                transaction_type=serializer.validated_data['transaction_type'],
                category=serializer.validated_data['category'],
                date=serializer.validated_data['date']
            )
            return Response({"detail": "Transaction created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailsView(APIView):
    """
    API view to retrieve, update or delete a specific transaction by ID.

    GET:
    Retrieve the details of a transaction by its ID.
    If the transaction is not found, return a 404 error.

    PUT:
    Update an existing transaction by its ID.
    If the transaction is not found, return a 404 error.
    Valid data must be provided for the update.

    DELETE:
    Delete a transaction by its ID.
    If the transaction is not found, return a 404 error.
    """

    @swagger_auto_schema(
        operation_description="Retrieve a transaction by ID",
        responses={
            200: TransactionSerializer(),
            404: openapi.Response('Transaction not found')
        }
    )
    def get(self, request: Request, id: uuid.UUID) -> Response:
        """
        Handle GET requests to retrieve a transaction by ID.

        This method retrieves the transaction via the `TransactionServiceImpl`, serializes it into JSON,
        and returns the serialized data in the response. If the transaction is not found, a 404 error is returned.
        """
        try:
            transaction = TransactionServiceImpl.get_transaction_by_id(id)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update a transaction by ID",
        request_body=TransactionSerializer,
        responses={
            200: openapi.Response('Transaction updated', TransactionSerializer),
            400: 'Bad Request',
            404: 'Transaction not found'
        }
    )
    def put(self, request: Request, id: uuid.UUID) -> Response:
        """
        Handle PUT requests to update a transaction by ID.

        This method takes the transaction data from the request, validates it using the `TransactionSerializer`,
        and updates the transaction through the `TransactionServiceImpl`. If the transaction is not found,
        a 404 error is returned.
        """
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                TransactionServiceImpl.update_transaction(id, **serializer.validated_data)
                return Response({'detail': 'Transaction updated'}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete a transaction by ID",
        responses={
            204: 'No Content',
            404: openapi.Response('Transaction not found')
        }
    )
    def delete(self, request: Request, id: uuid.UUID) -> Response:
        """
        Handle DELETE requests to delete a transaction by ID.

        This method deletes the transaction through the `TransactionServiceImpl`.
        If the transaction is not found, a 404 error is returned.
        """
        try:
            TransactionServiceImpl.delete_transaction(id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
