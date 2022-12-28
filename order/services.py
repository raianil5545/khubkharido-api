import dataclasses
import datetime
from product import services as product_services
from accounts import services as user_services
from typing import TYPE_CHECKING
from rest_framework import exceptions
from . import models as order_model
from django.shortcuts import get_object_or_404


if TYPE_CHECKING:
    from models import Order
    from accounts.models import User
    from product.models import Product


@dataclasses.dataclass
class OrderDataClass:
    name: str
    price: int
    quantity: int
    order_status: str = None
    date_placed: datetime.datetime = None
    id: int = None
    product: product_services.ProductDataClass = None
    user: user_services.UserDataClass = None

    @classmethod
    def from_instance(cls, order_model: "Order") -> "OrderDataClass":
        return cls(
            name=order_model.name,
            price=order_model.price,
            quantity=order_model.quantity,
            date_placed=order_model.date_placed,
            order_status=order_model.order_status,
            id=order_model.id,
            product=order_model.product,
            user=order_model.user
        )


def create_order(user, product, order: "OrderDataClass") -> "OrderDataClass":
    if user.role == "buyer":
        order_create = order_model.Order.objects.create(
            name=order.name,
            price=order.price,
            quantity=order.quantity,
            date_placed=order.date_placed,
            product=product,
            order_status="placed",
            user=user
        )
        return OrderDataClass.from_instance(order_model=order_create)
    else:
        raise exceptions.PermissionDenied("Unauthorized user")


def get_user_order(user: 'User') -> 'list["OrderDataClass"]':
    user_order_list = order_model.Order.objects.filter(user=user)
    return [OrderDataClass.from_instance(order) for order in user_order_list]


def get_order_by_id(order_id: int) -> "OrderDataClass":
    user_order = get_object_or_404(order_model.Order, pk=order_id)
    return OrderDataClass.from_instance(user_order)