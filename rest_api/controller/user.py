# Controller for user CRUD operations
from fastapi import APIRouter, HTTPException
import sys

sys.path.append("..")
from model.user import User

# Define a router to manage user-related routes
router = APIRouter()

# In-memory database to store user data
fake_users_db = []
user_id_counter = 1


# Create a new user
@router.post("/", response_model=User)
def create_user(user: User):
    """
    Create a new user.

    Args:
        user (User): User data to create.

    Returns:
        User: The created user.

    Raises:
        HTTPException: If the user cannot be created.
    """
    global user_id_counter

    new_user = User(id=user_id_counter, username=user.username, password=user.password)
    fake_users_db.append(new_user)
    user_id_counter += 1

    return new_user


# Get a list of all users
@router.get("/", response_model=list[User])
def read_users():
    """
    Get a list of all users.

    Returns:
        List[User]: A list of all users.
    """
    return fake_users_db


# Get a user by ID
@router.get("/{user_id}", response_model=User)
def read_user(user_id: int):
    """
    Get a user by ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: The user with the specified ID.

    Raises:
        HTTPException: If the user is not found.
    """
    user = find_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Update a user
@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: User):
    """
    Update a user's information.

    Args:
        user_id (int): The ID of the user to update.
        user_update (User): User data to update.

    Returns:
        User: The updated user.

    Raises:
        HTTPException: If the user is not found.
    """
    user = find_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)

    return user


# Delete a user
@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int):
    """
    Delete a user by ID.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        User: The deleted user.

    Raises:
        HTTPException: If the user is not found.
    """
    user = find_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    fake_users_db.remove(user)
    return user


def find_user_by_id(user_id: int):
    for user in fake_users_db:
        if user.id == user_id:
            return user
    return None
