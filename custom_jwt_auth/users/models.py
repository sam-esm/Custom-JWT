# Stdlib imports
from datetime import datetime, timedelta

# Core Django imports
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
# Third-party app imports
import jwt

# Imports from apps
from utils.models_mixins import TimeStampedModel


class UserManager(BaseUserManager):
    """
    A custom user manager where a phone number is the unique identifiers for authentication
    instead of usernames.
    """

    def create_user(self, phone_number, username=None, password=None):
        """
        Create and save a User with the given phone number, username and password.

        Args:
            phone_number (str): User's phone number. Must be unique.
            username (str, optional): User's username. Defaults to None.
            password (str, optional): User's password. Defaults to None.

        Raises:
            TypeError: If phone_number is None.

        Returns:
            User: The created User object.
        """

        if phone_number is None:
            raise TypeError("Users must have a phone number.")

        user = self.model(username=username, phone_number=phone_number)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, phone_number, password):
        """
        Create and save a SuperUser with the given username, phone number and password.

        Args:
            username (str): SuperUser's username.
            phone_number (str): SuperUser's phone number. Must be unique.
            password (str): SuperUser's password.

        Raises:
            TypeError: If password or username is None.

        Returns:
            User: The created SuperUser object.
        """
        # Check if password and username are provided
        if password is None:
            raise TypeError("Superusers must have a password.")
        if username is None:
            raise TypeError("Superusers must have a username.")

        user = self.create_user(username, phone_number, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """
    A custom User model where a phone number is the unique identifier
    for authentication instead of usernames.
    """

    phone_regex = RegexValidator(
        regex=r"^09\d{9}$|^9\d{9}$",
        message="Phone number must be either 11 digits and start with 0, or 10 digits and start with 9",
    )

    username = models.CharField(db_index=True, max_length=255, unique=True, null=True)
    phone_number = models.CharField(
        validators=[
            RegexValidator(
                regex=r"^0\d{10}$|^9\d{9}$",
                message="Wrong phone number format!",
            )
        ],
        max_length=11,
        unique=True,
        db_index=True
    )  # Field name made lowercase.db_index=True, max_length=11, unique=True)
    first_name = models.CharField(
        _("Name of User"), max_length=255, null=True, blank=True
    )
    last_name = models.CharField(
        _("LASTNAME of User"), max_length=255, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # The field that will be used for authentication
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username"]
    # The custom manager for this model
    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.
        """
        return str(self.phone_number)

    @property
    def token(self):
        """
        Returns the JWT token for this user.
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=6)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
