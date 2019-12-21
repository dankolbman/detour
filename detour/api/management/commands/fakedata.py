from django.core.management.base import BaseCommand, CommandError
from detour.api.factories import TripFactory, PointFactory


class Command(BaseCommand):
    help = "Make fake data"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("-n", help="number of points to make", type=int)

    def handle(self, *args, **options):
        n = options.get("n")
        if not n:
            n = 500
        t = TripFactory()
        PointFactory.create_batch(n, trip=t)
