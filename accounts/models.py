from django.db import models
from django.contrib.auth import models as auth_models

ROLE_CHOICES = (
    ("seller", "seller"),
    ("buyer", "buyer")
)


class UserManager(auth_models.BaseUserManager):
    def create_user(self, first_name: str, last_name: str, email: str, role: str = None, password: str = None,  is_staff=False, is_superuser=False) -> "User":
        if not email:
            raise ValueError("User must have email")
        if not first_name:
            raise ValueError("User must have first Name")
        if not last_name:
            raise ValueError("User must have last Name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.role = role
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(self, first_name: str, last_name: str, email: str, password: str) -> "User":
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )

        user.save()
        return user

class User(auth_models.AbstractUser):
    first_name = models.CharField(verbose_name="First Name", max_length=255)
    last_name = models.CharField(verbose_name="last Name", max_length=255)
    username = None
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    password = models.CharField(verbose_name="Password", max_length=255)
    role = models.CharField(verbose_name="Role", max_length=20, choices=ROLE_CHOICES, null=True)

    object = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


