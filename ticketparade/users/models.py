from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .constants import DEFAULT_COLUMNS_IN_THEATER
from .constants import DEFAULT_ROWS_IN_THEATER
from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for TicketParade.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]
    email = models.EmailField(_("email address"), unique=True)
    username = None  # type: ignore[assignment]

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})


class Theater(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=32, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)
    number_of_rows = models.IntegerField(default=DEFAULT_ROWS_IN_THEATER)
    number_of_columns = models.IntegerField(default=DEFAULT_COLUMNS_IN_THEATER)

    def __str__(self):
        return self.name


class TheaterSeat(models.Model):
    theater = models.ForeignKey(
        "Theater",
        on_delete=models.CASCADE,
        related_name="seats",
    )
    seat_number = models.CharField(max_length=32)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ("theater", "seat_number")

    def __str__(self):
        return f"{self.theater.name} - {self.seat_number}"


class BooekedTheaterSeat(models.Model):
    theater_seat = models.ForeignKey(
        "TheaterSeat",
        on_delete=models.CASCADE,
        related_name="booked_seats",
    )
    email = models.EmailField(max_length=255)
    movie_id = models.IntegerField()

    class Meta:
        unique_together = ("theater_seat", "movie_id")
