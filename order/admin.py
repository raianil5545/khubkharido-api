from django.contrib import admin

from . import models

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "user",
        "name",
        "quantity",
        "order_status",
        "date_placed"
    )

admin.site.register(models.Order, OrderAdmin)