import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from product import models
from PIL import Image
import tempfile


@pytest.mark.django_db
def test_create_product(user_seller, auth_client):
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
    assert response.status_code == 200

    status_from_db = models.Product.objects.all().first()
    data = response.data
    assert data["name"] == status_from_db.name
    assert data["id"] == status_from_db.id
    assert data["user"]["id"] == user_seller.id


@pytest.mark.django_db
def test_create_product_fail_authorization(user_buyer, auth_client_buyer):
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
    response = auth_client_buyer.post("/api/product/", payload)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_user_product(auth_client, user_seller):
    small_gif1 = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded1 = SimpleUploadedFile('small1.gif', small_gif1, content_type='image/gif')
    payload1 = dict(
        name="some name",
        description="some description",
        price=200,
        in_stock=10,
        brands=["test", "no brands"],
        categories=["winter", "wear"],
        images=uploaded1
    )
    small_gif2 = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded2 = SimpleUploadedFile('small2.gif', small_gif2, content_type='image/gif')
    payload2 = dict(
        name="some other name",
        description="some other description",
        price=200,
        in_stock=10,
        brands=["test", "no brands"],
        categories=["winter", "wear"],
        images=uploaded2
    )
    models.Product.objects.create(user_id=user_seller.id, **payload1)
    models.Product.objects.create(user_id=user_seller.id, **payload2)
    response = auth_client.get('/api/product/')
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_get_product_404(auth_client):
    response = auth_client.get('/api/product/0/')
    assert response.status_code == 404

@pytest.mark.django_db
def test_update_product_by_id(auth_client, user_seller):
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
        images=uploaded)
    product = models.Product.objects.create(user_id=user_seller.id, **payload)
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    file = tempfile.NamedTemporaryFile(suffix='.png')
    image.save(file)
    with open(file.name, 'rb') as data:
        payload2 = dict(
            name="some other name",
            description="some other description",
            price=20,
            in_stock=10,
            brands=["test", "rest"],
            categories=["winter", "wear"],
            images=data
        )
        response = auth_client.put(f"/api/product/{product.id}/", payload2,  format='multipart')
    product.refresh_from_db()
    assert response.status_code == 200
    data = response.data
    assert data["id"] == product.id


@pytest.mark.django_db
def test_delete_product(auth_client, user_seller):
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
        images=uploaded)
    product = models.Product.objects.create(user_id=user_seller.id, **payload)
    response = auth_client.delete(f"/api/product/{product.id}/")
    assert response.status_code == 204




