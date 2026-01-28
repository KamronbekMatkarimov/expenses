from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        OWNER = "owner", "Owner"
        ACCOUNTANT = "accountant", "Accountant"
        ANALYST = "analyst", "Analyst"

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.OWNER,
        help_text="User role for permissions (owner/accountant/analyst)",
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_users",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
    )

    def __str__(self):
        return self.username
