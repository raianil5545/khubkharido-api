from django.contrib import admin

from . import models

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "user",
        "price",
        "in_stock",
        "brands",
        "categories",
        "images"
    )

admin.site.register(models.Product, ProductAdmin)