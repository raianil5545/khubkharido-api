import pytest
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts import services as user_services
from product.models import Product

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


@pytest.fixture
def product(auth_client):
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
    payload = dict(
        name="some name",
        description="some description",
        price=200,
        in_stock=10,
        brands=["test", "no brands"],
        categories=["winter", "wear"],
        images=uploaded
    )
    response = auth_client.post("/api/product/", payload)
    return response.data




