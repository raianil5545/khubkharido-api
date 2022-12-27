from django.contrib import admin
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "role"
    )


admin.site.register(models.User, UserAdmin)
