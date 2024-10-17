import uuid
import pytest
from django.urls import reverse
from rest_framework import status
from users_app.models import User
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_get_user_details_valid(api_client):
    """
    Test case: Retrieve user details by valid user ID.

    Scenario:
    - Create a user in the database.
    - Make a GET request to retrieve the user's details by ID.

    Expected Result:
    - The response status code is 200 (OK).
    - The response contains the user's email matching the created user's email.
    """
    user = User.objects.create(first_name="John", last_name="Doe", email="john@example.com")
    url = reverse('user-detail', args=[user.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == user.email


@pytest.mark.django_db
def test_get_user_details_invalid(api_client):
    """
    Test case: Attempt to retrieve user details by invalid user ID.

    Scenario:
    - Generate a random UUID that does not correspond to any user.
    - Make a GET request to retrieve the user's details by ID.

    Expected Result:
    - The response status code is 404 (Not Found).
    - The response contains a message indicating that the user was not found.
    """
    invalid_id = uuid.uuid4()
    url = reverse('user-detail', args=[invalid_id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == "User not found"


@pytest.mark.django_db
def test_update_user_valid(api_client):
    """
    Test case: Update user details with valid data.

    Scenario:
    - Create a user in the database.
    - Make a PUT request to update the user's first name and last name.

    Expected Result:
    - The response status code is 200 (OK).
    - The updated user's first name matches the new first name.
    """
    user = User.objects.create(first_name="John", last_name="Doe", email="john@example.com")
    url = reverse('user-detail', kwargs={'id': user.id})
    data = {
        "first_name": "UpdatedJohn",
        "last_name": "UpdatedDoe",
    }
    response = api_client.put(url, data=data, format='json')
    updated_user = User.objects.get(id=user.id)

    assert response.status_code == status.HTTP_200_OK
    assert updated_user.first_name == "UpdatedJohn"
    assert updated_user.last_name == "UpdatedDoe"


@pytest.mark.django_db
def test_update_user_invalid(api_client):
    """
    Test case: Attempt to update user details with invalid data.

    Scenario:
    - Create a user in the database.
    - Make a PUT request to update the user's first name to an empty string.

    Expected Result:
    - The response status code is 400 (Bad Request).
    - The response contains an error for the first name field.
    """
    user = User.objects.create(first_name="John", last_name="Doe", email="john@example.com")
    url = reverse('user-detail', args=[user.id])
    data = {
        "first_name": "",
    }
    response = api_client.put(url, data=data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "first_name" in response.data


@pytest.mark.django_db
def test_delete_user_valid(api_client):
    """
    Test case: Delete a user by valid user ID.

    Scenario:
    - Create a user in the database.
    - Make a DELETE request to remove the user by ID.

    Expected Result:
    - The response status code is 204 (No Content).
    - The user no longer exists in the database.
    """
    user = User.objects.create(first_name="John", last_name="Doe", email="john@example.com")
    url = reverse('user-detail', args=[user.id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_delete_user_invalid(api_client):
    """
    Test case: Attempt to delete a user by invalid user ID.

    Scenario:
    - Generate a random UUID that does not correspond to any user.
    - Make a DELETE request to remove the user by ID.

    Expected Result:
    - The response status code is 404 (Not Found).
    - The response contains a message indicating that the user was not found.
    """
    invalid_id = uuid.uuid4()
    url = reverse('user-detail', args=[invalid_id])
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'] == "User not found"
