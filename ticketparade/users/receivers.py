import logging

from django.dispatch import receiver

logger = logging.getLogger(__name__)

from .models import Theater
from .models import TheaterSeat


@receiver(post_save, sender=Theater)
def create_theater_seats(sender, instance, created, **kwargs):
    """
    Create theater seats for a new theater.
    Rows are alphabets from A to Z.
    Columns are numbers starts from 1.
    """
    if created:
        temporary_seats = []
        for row in range(instance.number_of_rows):
            for column in range(instance.number_of_columns):
                seat_number = chr(65 + row) + str(column + 1)
                temporary_seats.append(
                    TheaterSeat(theater=instance, seat_number=seat_number),
                )
        seats, created = TheaterSeat.objects.bulk_create(temporary_seats)
        logger.info(f"Created {len(temporary_seats)} seats for {instance.name}")
