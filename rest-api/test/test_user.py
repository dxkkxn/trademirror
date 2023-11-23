from httpx import AsyncClient
import pytest
import sys

sys.path.append("..")
from main import app
from model.user import User


@pytest.fixture
def test_client():
    # Create a test client to make HTTP requests
    return AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_create_user(test_client):
    # Define test user data
    test_user = User(id=0, username="testuser", password="testpassword")
    # Send a POST request to create the user
    response = await test_client.post("/user/", json=test_user.dict())
    # Check the response
    assert response.status_code == 200
    user = User(**response.json())
    assert user == test_user  # Compare the created user with the test data


@pytest.mark.asyncio
async def test_read_users(test_client):
    # Send a GET request to retrieve all users
    response = await test_client.get("/user/")

    # Check the response
    assert response.status_code == 200
    users = [User(**user) for user in response.json()]
    assert len(users) > 0


@pytest.mark.asyncio
async def test_read_user(test_client):
    # Define test user data
    test_user = User(id=1, username="testuser", password="testpassword")

    # Create the test user by sending a POST request
    response = await test_client.post("/user/", json=test_user.dict())
    created_user = User(**response.json())

    # Send a GET request to retrieve the created user
    response = await test_client.get(f"/user/{created_user.id}")

    # Check the response
    assert response.status_code == 200
    user = User(**response.json())
    assert user == created_user


@pytest.mark.asyncio
async def test_update_user(test_client):
    # Define test user data
    test_user = User(id=2, username="testuser", password="testpassword")

    # Create the test user by sending a POST request
    response = await test_client.post("/user/", json=test_user.dict())
    print(response)
    created_user = User(**response.json())

    # Define updated user data
    updated_user_data = {
        "username": "updateduser",
        "password": "updatedpassword",
    }

    # Send a PUT request to update the user
    response = await test_client.put(f"/user/{created_user.id}", json=updated_user_data)

    # Check the response
    assert response.status_code == 200
    user = User(**response.json())
    assert user.username == updated_user_data["username"]
    assert user.password == updated_user_data["password"]


@pytest.mark.asyncio
async def test_delete_user(test_client):
    # Define test user data
    test_user = User(id=3, username="testuser", password="testpassword")

    # Create the test user by sending a POST request
    response = await test_client.post("/user/", json=test_user.dict())
    created_user = User(**response.json())

    # Send a DELETE request to delete the user
    response = await test_client.delete(f"/user/{created_user.id}")
    print(response)

    # Check the response
    assert response.status_code == 200

    # Verify that the user has been deleted by sending a GET request
    response = await test_client.get(f"/user/{created_user.id}")
    assert response.status_code == 404
