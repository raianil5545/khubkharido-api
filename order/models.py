from django.db import models
from product.models import Product
from django.core.validators import MaxValueValidator
from django.conf import settings


ORDER_CHOICES = (
    ("processing", "processing"),
    ("canceled", "canceled"),
    ("on hold", "on hold"),
    ("refunded", "refunded"),
    ("placed", "placed")
)


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="product_id")
    name = models.CharField(max_length=250, verbose_name="product name")
    price = models.PositiveIntegerField(verbose_name="price", validators=(MaxValueValidator, ))
    quantity = models.PositiveSmallIntegerField(verbose_name="quantity of purchased")
    order_status = models.CharField(default="placed", max_length=50, choices=ORDER_CHOICES, verbose_name="order status")
    date_placed = models.DateTimeField(auto_now_add=True, verbose_name="date ordered")


