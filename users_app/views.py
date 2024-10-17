import uuid

from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from users_app.serializers import UserSerializer
from users_app.service.user_service_impl import UserServiceImpl


class UserListView(APIView):
    """
    API View to handle the retrieval and creation of users.

    Methods:
    - GET: Retrieve a list of all users in the system.
    - POST: Create a new user using the provided data.
    """

    @swagger_auto_schema(
        operation_description="Retrieve a list of all users",
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request: Request) -> Response:
        """
        Handle GET requests to return a list of all users.

        This method retrieves all users from the database via the `UserServiceImpl` service,
        serializes them into JSON, and returns the serialized data in the response.
        """
        users = UserServiceImpl.get_all_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=UserSerializer,
        responses={
            201: openapi.Response('User created', UserSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request: Request) -> Response:
        """
        Handle POST requests to create a new user.

        This method takes the user data from the request, validates it using the `UserSerializer`,
        and if valid, creates a new user through the `UserServiceImpl` service. If the data is
        invalid, it returns the validation errors.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            UserServiceImpl.save_new_user(serializer.validated_data['first_name'],
                                                 serializer.validated_data['last_name'],
                                                 serializer.validated_data['email'])
            return Response({"detail": "User created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailsView(APIView):
    """
    API View to handle retrieval, update, and deletion of a user by ID.

    Methods:
    - GET: Retrieve user by ID.
    - PUT: Update user by ID.
    - DELETE: Delete user by ID.
    """

    @swagger_auto_schema(
        operation_description="Retrieve user by ID",
        responses={200: UserSerializer(), 404: 'User not found'}
    )
    def get(self, request: Request, id: uuid.UUID) -> Response:
        """
        Handle GET requests to return user details by ID.

        This method retrieves a user by ID from the database via the `UserServiceImpl` service,
        serializes the user into JSON, and returns the serialized data in the response.
        """
        try:
            user = UserServiceImpl.get_user_by_id(id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update user by ID",
        request_body=UserSerializer,
        responses={
            200: openapi.Response('User updated', UserSerializer),
            400: 'Bad Request',
            404: 'User not found'
        }
    )
    def put(self, request: Request, id: uuid.UUID) -> Response:
        """
        Handle PUT requests to update a user by ID.

        This method takes user data from the request, validates it using the `UserSerializer`,
        and updates the user through the `UserServiceImpl` service. Returns validation errors
        if the input data is invalid.
        """
        try:
            serializer = UserSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                UserServiceImpl.update_existing_user(
                    user_id=id,
                    **serializer.validated_data
                )
                return Response({"detail": "User updated"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Delete user by ID",
        responses={204: 'No Content', 404: 'User not found'}
    )
    def delete(self, request: Request, id: uuid.UUID) -> Response:
        """
        Handle DELETE requests to delete a user by ID.

        This method deletes a user by ID through the `UserServiceImpl` service.
        """
        try:
            UserServiceImpl.delete_user(id)
            return Response({"detail": "Successfully deleted user"}, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
