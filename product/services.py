import dataclasses
import datetime
from accounts import services as user_service
from typing import TYPE_CHECKING
from django.shortcuts import get_object_or_404
from rest_framework import exceptions

from . import models as product_models

if TYPE_CHECKING:
    from models import Product
    from accounts.models import User


@dataclasses.dataclass
class ProductDataClass:
    name: str
    description: str
    price: int
    in_stock: int
    brands: list
    categories: list
    images: bytearray
    user: user_service.UserDataClass = None
    id: int = None
    created_at: datetime.datetime = None

    @classmethod
    def from_instance(cls, product_model: "Product") -> "ProductDataClass":
        return cls(
            name=product_model.name,
            description=product_model.description,
            price=product_model.price,
            in_stock=product_model.in_stock,
            brands=product_model.brands,
            categories=product_model.categories,
            images=product_model.images,
            id=product_model.id,
            created_at=product_model.created_at,
            user=product_model.user
        )


def create_product(user, product: "ProductDataClass") -> "ProductDataClass":
    if user.role == "seller":
        product_create = product_models.Product.objects.create(
            name=product.name,
            description=product.description,
            price=product.price,
            in_stock=product.in_stock,
            brands=product.brands,
            categories=product.categories,
            images=product.images,
            user=user
        )
        return ProductDataClass.from_instance(product_model=product_create)
    else:
        raise exceptions.PermissionDenied("Unauthorized, only seller can create product")


def get_user_product(user: "User") -> 'list["ProductDataClass"]':
    user_products = product_models.Product.objects.filter(user=user)

    return [ProductDataClass.from_instance(product) for product in user_products]


def get_product_by_id(product_id: int) -> "ProductDataClass":
    product_by_id = get_object_or_404(product_models.Product, pk=product_id)
    return ProductDataClass.from_instance(product_model=product_by_id)


def delete_product_by_id(user: "User", product_id: int) -> "ProductDataClass":
    product = get_object_or_404(product_models.Product, pk=product_id, user=user)
    if user.id != product.user.id:
        raise exceptions.PermissionDenied("Unauthorized Delete")
    product.delete()


def update_product_by_id(user: "User", product_id: int, product_data: "ProductDataClass") -> 'ProductDataClass':
    product = get_object_or_404(product_models.Product, pk=product_id, user=user)
    if user.id != product.user.id:
        raise exceptions.PermissionDenied("Unauthorized Update")
    product.name = product_data.name
    product.description = product_data.description
    product.price = product_data.price
    product.in_stock = product_data.in_stock
    product.brands = product_data.brands
    product.categories = product_data.categories
    product.images = product_data.images
    product.save()
    return ProductDataClass.from_instance(product_model=product)
