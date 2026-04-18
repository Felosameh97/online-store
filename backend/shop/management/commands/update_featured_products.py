from django.core.management.base import BaseCommand
from shop.services import update_featured_products


class Command(BaseCommand):
    help = "Update featured product flags based on recent best-selling products."

    def handle(self, *args, **options):
        update_featured_products(days=30, limit=12)
        self.stdout.write(self.style.SUCCESS("Featured products updated successfully."))
