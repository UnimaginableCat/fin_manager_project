import uuid
from unittest import mock

import pytest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist
from users_app.models import User
from users_app.service.user_service_impl import UserServiceImpl


@pytest.fixture
def user_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com"
    }


@pytest.fixture
def user_entity() -> User:
    return User(id=uuid.uuid4(), first_name="John", last_name="Doe", email="johndoe@example.com")


@mock.patch.object(User, "save")
def test_save_new_user(mock_user_save: MagicMock, user_data, user_entity):
    """Test saving a new user successfully.

    This test mocks the save method of the User model and asserts that
    the method is called once when saving a new user.
    """
    mock_user_save.return_value = user_entity
    result = UserServiceImpl.save_new_user(user_data['first_name'], user_data['last_name'], user_data['email'])
    mock_user_save.assert_called_once()
    assert result == mock_user_save.return_value


@mock.patch.object(User, "save")
def test_save_new_user_fail(mock_user_save: MagicMock, user_data):
    """Test saving a new user fails due to a database error.

    This test mocks the save method to raise an exception and checks
    that the exception is correctly raised.
    """
    mock_user_save.side_effect = Exception("Database error")
    with pytest.raises(Exception, match="Database error"):
        UserServiceImpl.save_new_user(user_data['first_name'], user_data['last_name'], user_data['email'])
    mock_user_save.assert_called_once()


@mock.patch.object(User, "save")
@mock.patch.object(User, "objects")
def test_update_existing_user(mock_user_objects: MagicMock, mock_user_save: MagicMock, user_data, user_entity):
    """Test updating an existing user successfully.

    This test checks that the update_existing_user method calls the
    get method and save method of the User model correctly, and asserts
    that the returned user has the updated first name.
    """
    updated_name = 'updatedName'
    user_id = user_entity.id

    mock_user_objects.get.return_value = user_entity
    mock_user_save.return_value = User(id=user_entity.id,
                                       first_name=updated_name,
                                       last_name=user_entity.last_name,
                                       email=user_entity.email)

    result = UserServiceImpl.update_existing_user(user_id, first_name=updated_name)

    mock_user_objects.get.assert_called_once_with(id=user_id)
    mock_user_save.assert_called_once()

    assert result.first_name == updated_name


@mock.patch.object(User, "objects")
def test_update_existing_user_not_found(mock_user_objects: MagicMock, user_entity):
    """Test updating an existing user fails when user is not found.

    This test checks that attempting to update a user that does not exist
    raises an ObjectDoesNotExist exception.
    """
    mock_user_objects.get.side_effect = ObjectDoesNotExist("Not Found")

    with pytest.raises(ObjectDoesNotExist):
        UserServiceImpl.update_existing_user(user_entity.id,
                                             first_name = user_entity.first_name,
                                             last_name = user_entity.last_name,
                                             email = user_entity.email)

    mock_user_objects.get.assert_called_once_with(id=user_entity.id)


@mock.patch.object(User, "delete")
@mock.patch.object(User, "objects")
def test_delete_user(mock_user_objects: MagicMock, mock_user_delete: MagicMock, user_entity):
    """Test deleting an existing user successfully.

    This test verifies that the delete_user method correctly calls the
    delete method of the User model for the given user.
    """
    mock_user_objects.get.return_value = user_entity

    UserServiceImpl.delete_user(user_entity.id)
    mock_user_delete.assert_called_once()


@mock.patch.object(User, "delete")
@mock.patch.object(User, "objects")
def test_delete_user_not_found(mock_user_objects: MagicMock, mock_user_delete: MagicMock, user_entity):
    """Test deleting a user fails when user is not found.

    This test checks that attempting to delete a user that does not exist
    raises an ObjectDoesNotExist exception.
    """
    mock_user_objects.get.side_effect = ObjectDoesNotExist("Not Found")

    with pytest.raises(ObjectDoesNotExist):
        UserServiceImpl.delete_user(user_entity.id)

    mock_user_objects.get.assert_called_once_with(id=user_entity.id)
    mock_user_delete.assert_not_called()


@mock.patch.object(User, "objects")
def test_get_all_users(mock_user_objects: MagicMock, user_entity):
    """Test retrieving all users.

    This test mocks the all method of the User model and asserts that
    it returns the correct number of users.
    """
    mock_user_objects.all.return_value = [user_entity]
    result = UserServiceImpl.get_all_users()
    mock_user_objects.all.assert_called_once()
    assert len(result) == len(mock_user_objects.all.return_value)


@mock.patch.object(User, "objects")
def test_get_user_by_id(mock_user_objects: MagicMock, user_entity):
    """Test retrieving a user by ID successfully.

    This test checks that the get_user_by_id method correctly retrieves
    the user for the given ID.
    """
    mock_user_objects.get.return_value = user_entity
    result = UserServiceImpl.get_user_by_id(user_entity.id)

    mock_user_objects.get.assert_called_once_with(id=user_entity.id)
    assert result == user_entity


@mock.patch.object(User, "objects")
def test_get_user_by_id_not_found(mock_user_objects: MagicMock, user_entity):
    """Test retrieving a user by ID fails when user is not found.

    This test checks that attempting to retrieve a user that does not exist
    raises an ObjectDoesNotExist exception.
    """
    mock_user_objects.get.side_effect = ObjectDoesNotExist("Not Found")
    with pytest.raises(ObjectDoesNotExist):
        UserServiceImpl.get_user_by_id(user_entity.id)

    mock_user_objects.get.assert_called_once_with(id=user_entity.id)
