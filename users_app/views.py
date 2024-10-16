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

    Usage:
    - GET /users/: Returns a list of all users serialized as JSON.
    - POST /users/: Accepts a JSON payload with 'first_name', 'last_name', and 'email'
      to create a new user. Returns the newly created user or validation errors.
    """
    def get(self, request: Request) -> Response:
        """
        Handle GET requests to return a list of all users.

        This method retrieves all users from the database via the `UserServiceImpl` service,
        serializes them into JSON, and returns the serialized data in the response.

        Args:
        - request (Request): The request object containing HTTP request data.

        Returns:
        - Response: A JSON response containing a list of serialized user objects.
        """
        users = UserServiceImpl.get_all_users()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        """
        Handle POST requests to create a new user.

        This method takes the user data from the request, validates it using the `UserSerializer`,
        and if valid, creates a new user through the `UserServiceImpl` service. If the data is
        invalid, it returns the validation errors.

        Args:
        - request (Request): The request object containing HTTP request data with user information.

        Returns:
        - Response: A JSON response containing the newly created user or validation errors.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = UserServiceImpl.save_new_user(serializer.validated_data['first_name'],
                                                 serializer.validated_data['last_name'],
                                                 serializer.validated_data['email'])
            return Response(user, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
