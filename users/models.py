import random
import string
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    is_freelancer = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)

    email_verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Track email verification status

    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions_set", blank=True)

    def __str__(self):
        return self.email  # Use email instead of username

    def generate_verification_code(self):
        """Generate a random 6-digit verification code and save it."""
        code = ''.join(random.choices(string.digits, k=6))  # Generate 6-digit code
        self.email_verification_code = code
        self.save()
        return code
