# Generated by Django 4.1.4 on 2022-12-28 10:43

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models
import product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, verbose_name="product name")),
                ("description", models.TextField(verbose_name="product description")),
                (
                    "price",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MaxValueValidator(200000)],
                        verbose_name="price",
                    ),
                ),
                (
                    "in_stock",
                    models.PositiveSmallIntegerField(verbose_name="Quantity in stock"),
                ),
                (
                    "brands",
                    django_mysql.models.ListCharField(
                        models.CharField(max_length=20),
                        max_length=126,
                        size=5,
                        verbose_name="product brands",
                    ),
                ),
                (
                    "categories",
                    django_mysql.models.ListCharField(
                        models.CharField(max_length=25),
                        max_length=156,
                        size=5,
                        verbose_name="product categories",
                    ),
                ),
                ("images", models.ImageField(upload_to=product.models.upload_path)),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date Published"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
        ),
    ]
