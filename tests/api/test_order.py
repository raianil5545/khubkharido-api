import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from product.models import Product
from order.models import Order



@pytest.mark.django_db
def test_post_order(user_seller, auth_client_buyer):
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

    product = Product.objects.create(user_id=user_seller.id, **payload)

    order_payload = dict(
        name="some name",
        price=200,
        quantity=1,
        product_id=product.id
    )

    response = auth_client_buyer.post(f"/api/order/", order_payload)
    assert response.status_code == 200
    assert response.data["name"] == "some name"

@pytest.mark.django_db
def test_get_order_list(user_seller, user_buyer, auth_client_buyer):
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
    product_payload = dict(
        name="some name",
        description="some description",
        price=200,
        in_stock=10,
        brands=["test", "no brands"],
        categories=["winter", "wear"],
        images=uploaded)
    order_payload = dict(
        name="some name",
        price=200,
        quantity=1,
        )

    product = Product.objects.create(user_id=user_seller.id, **product_payload)
    Order.objects.create(user_id=user_buyer.id, product_id=product.id, **order_payload)

    response = auth_client_buyer.get(f"/api/order/")
    assert response.status_code == 200
    assert len(response.data) == 1
@pytest.mark.django_db
def test_get_order_id(user_seller, user_buyer, auth_client_buyer):
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
    product_payload = dict(
        name="some name",
        description="some description",
        price=200,
        in_stock=10,
        brands=["test", "no brands"],
        categories=["winter", "wear"],
        images=uploaded)
    order_payload = dict(
        name="some name",
        price=200,
        quantity=1,
        )

    product = Product.objects.create(user_id=user_seller.id, **product_payload)
    order = Order.objects.create(user_id=user_buyer.id, product_id=product.id, **order_payload)

    response = auth_client_buyer.get(f"/api/order/{order.id}/")
    assert response.status_code == 200
    assert response.data["id"] == order.id

@pytest.mark.django_db
def test_put_order_id(user_seller, user_buyer, auth_client_buyer):
    small_gif = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    uploaded = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')
    product_payload = dict(
        name="some name",
        description="some description",
        price=200,
        in_stock=10,
        brands=["test", "no brands"],
        categories=["winter", "wear"],
        images=uploaded)
    order_payload = dict(
        name="some name",
        price=200,
        quantity=1,
        )

    product = Product.objects.create(user_id=user_seller.id, **product_payload)
    order = Order.objects.create(user_id=user_buyer.id, product_id=product.id, **order_payload)

    updated_order = dict(
        order_status="processing",
        pk=order.id
    )

    response = auth_client_buyer.put(f"/api/order/update/{order.id}/", updated_order)
    assert response.status_code == 200
    assert response.data["id"] == order.id
    assert response.data["order_status"] == "processing"
