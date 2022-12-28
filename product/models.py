from django.db import models
from django.conf import settings
from django_mysql.models import ListCharField
from django.core.validators import MaxValueValidator
from datetime import date


def upload_path(instance, title):
    today = str(date.today())
    username = instance.user
    return f'product_images/{username}/{today}' + title


class Product(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user"
    )
    name = models.CharField(verbose_name="product name", max_length=200)
    description = models.TextField(verbose_name="product description")
    price = models.PositiveIntegerField(verbose_name="price", validators=(MaxValueValidator(200000), ))
    in_stock = models.PositiveSmallIntegerField(verbose_name="Quantity in stock")
    brands = ListCharField(verbose_name="product brands",
                           base_field=models.CharField(max_length=20),
                           size=5,
                           max_length=(21*6))
    categories = ListCharField(verbose_name="product categories",
                               base_field=models.CharField(max_length=25),
                               size=5,
                               max_length=(26*6))
    images = models.ImageField(upload_to=upload_path)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Published")



