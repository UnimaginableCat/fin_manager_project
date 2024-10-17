import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users_app.models import User

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_get_user_list(api_client):
    """
    Test case: Retrieve a list of users via GET request.

    Scenario:
    - Create two users in the database.
    - Make a GET request to retrieve the list of users.

    Expected Result:
    - The response status code is 200 (OK).
    - The response contains a list of users with a length of 2.
    """
    User.objects.create(first_name="John", last_name="Doe", email="john@example.com")
    User.objects.create(first_name="Jane", last_name="Smith", email="jane@example.com")

    url = reverse('users')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2

@pytest.mark.django_db
def test_create_user_valid(api_client):
    """
    Test case: Create a new user via POST request with valid data.

    Scenario:
    - Send a POST request with valid user data (first name, last name, and email).

    Expected Result:
    - The response status code is 201 (Created).
    """
    url = reverse('users')
    data = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice@example.com"
    }
    response = api_client.post(url, data=data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_create_user_invalid(api_client):
    """
    Test case: Attempt to create a new user via POST request with invalid data.

    Scenario:
    - Send a POST request with an empty 'first_name' field, which is invalid.

    Expected Result:
    - The response status code is 400 (Bad Request).
    - The response contains a validation error for the 'first_name' field.
    """
    url = reverse('users')
    data = {
        "first_name": "",
        "last_name": "Johnson",
        "email": "alice@example.com"
    }
    response = api_client.post(url, data=data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "first_name" in response.data
