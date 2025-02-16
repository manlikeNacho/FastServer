from unittest.mock import patch, MagicMock
import pytest
from datetime import datetime, timedelta, timezone
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User, Base
from app.schema import UserLogin, CreateUser, UserResp
from app.oauth2 import create_access_token, verify_access_token, TokenData
from app.utils import hash, verify_password, get_password_hash
from fastapi.testclient import TestClient
from app.main import app

# Test client for FastAPI
client = TestClient(app)

# Fixtures for reusable test objects


@pytest.fixture
def mock_db_session():
    return MagicMock(spec=Session)


@pytest.fixture
def sample_user():
    user_id = uuid4()
    return User(
        id=user_id,
        name="John Doe",
        email="john.doe@example.com",
        address="123 Main St",
        password="hashedpassword",
        created_at=datetime.now()
    )


@pytest.fixture
def sample_user_credentials():
    return UserLogin(email="john.doe@example.com", password="testpassword")


@pytest.fixture
def sample_create_user():
    return CreateUser(
        name="John Doe",
        email="john.doe@example.com",
        address="123 Main St",
        password="testpassword"
    )

# Test models


def test_user_model(sample_user):
    assert isinstance(sample_user.id, uuid4().__class__)  # Check if ID is UUID
    assert sample_user.name == "John Doe"
    assert sample_user.email == "john.doe@example.com"
    assert sample_user.address == "123 Main St"
    assert sample_user.password == "hashedpassword"
    assert isinstance(sample_user.created_at, datetime)


# Test router endpoints


def test_login_success(mock_db_session, sample_user_credentials):
    # Mock the hash and verify_password functions
    with patch("app.utils.hash", return_value="mocked_hashed_password"), \
            patch("app.utils.verify_password", return_value=True):

        # Mock the database response
        user_id = uuid4()
        mock_db_session.query.return_value.filter.return_value.first.return_value = User(
            id=user_id,
            email="john.doe@example.com",
            password="testpassword"
        )

        # Call the login endpoint
        response = client.post(
            "/auth/login", json=sample_user_credentials.model_dump())

        # Assert the response
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"


def test_create_and_verify_access_token():
    user_id = str(uuid4())  # Convert UUID to string for JWT
    token = create_access_token(data={"user_id": str(user_id)})
    assert token is not None

    # Verify the token
    token_data = verify_access_token(token, HTTPException(
        status_code=401, detail="Could not validate credentials"))
    assert token_data.user_id == user_id

    # Test expired token
    expired_token = create_access_token(
        data={"user_id": user_id}, expires_delta=timedelta(minutes=-1))
    with pytest.raises(HTTPException) as exc_info:
        verify_access_token(expired_token, HTTPException(
            status_code=401, detail="Could not validate credentials"))
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"


# def test_login_invalid_credentials(mock_db_session, sample_user_credentials):
#     # Mock the hash and verify_password functions
#     with patch("app.utils.hash", return_value="mocked_hashed_password"), \
#             patch("app.utils.verify_password", return_value=False):

#         # Mock the database response
#         user_id = uuid4()
#         mock_db_session.query.return_value.filter.return_value.first.return_value = User(
#             id=user_id,
#             email="john.doe@example.com",
#             password="mocked_hashed_passwordd"  # Use the mocked hash
#         )

#         # Call the login endpoint
#         response = client.post(
#             "/auth/login", json=sample_user_credentials.model_dump())

#         # Assert the response
#         assert response.status_code == 401


# def test_register_user(mock_db_session, sample_create_user):
#     user_id = uuid4()
#     mock_db_session.add.return_value = None
#     mock_db_session.commit.return_value = None
#     mock_db_session.refresh.return_value = User(
#         id=user_id,
#         name="John Doee",
#         email="john.doe3@example.com",
#         address="123 Main St",
#         password="testpassword",
#         created_at=datetime.now()
#     )
#     response = client.post(
#         "/auth/register", json=sample_create_user.model_dump())
#     assert response.status_code == 200
#     # Ensure UUID is returned as string
#     assert response.json()["id"] == str(user_id)
#     assert response.json()["email"] == "john.doe3@example.com"


def test_register_user_failure(mock_db_session, sample_create_user):
    mock_db_session.add.side_effect = Exception("Database error")
    response = client.post(
        "/auth/register", json=sample_create_user.model_dump())
    assert response.status_code == 400
