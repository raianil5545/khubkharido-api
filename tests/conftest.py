import pytest
from rest_framework.test import APIClient

from accounts import services as user_services

@pytest.fixture
def user_seller():
    user_dc = user_services.UserDataClass(
        first_name="Test",
        last_name="seller",
        email="testseller@gmail.com",
        password="TestSeller",
        role="seller"
    )
    user_seller = user_services.create_user(user_dc=user_dc)
    return user_seller


@pytest.fixture
def user_buyer():
    user_dc = user_services.UserDataClass(
        first_name="Test",
        last_name="buyer",
        email="testbuyer@gmail.com",
        password="TestBuyer",
        role="buyer"
    )
    user_buyer = user_services.create_user(user_dc=user_dc)
    return user_buyer

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def auth_client(user_seller, client):
    client.post("/api/user/login/", dict(email="testseller@gmail.com", password="TestSeller", ))
    return client

@pytest.fixture
def auth_client_buyer(user_buyer, client):
    client.post("/api/user/login/", dict(email="testbuyer@gmail.com", password="TestBuyer", ))
    return client



