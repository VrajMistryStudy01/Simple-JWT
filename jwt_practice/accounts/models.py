from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Uses email as the unique identifier instead of username.
    """
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name="customuser_groups")  # ✅ Add related_name
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions")  # ✅ Add related_name

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
