"""database models"""

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(
        self, email, password=None, **extra_fields
    ):  # will create extra fields in the db if needed.
        """Create, save and return new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # get the password and encrypts it.
        user.save(using=self._db)  # this is just a best practice
        return user  # Return the user object

    def create_superuser(self, email, password):
        """Create and return a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user  # Return the user object


class User(AbstractBaseUser, PermissionsMixin):
    """user in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # this is how you assign a user manager in django.

    USERNAME_FIELD = "email"
