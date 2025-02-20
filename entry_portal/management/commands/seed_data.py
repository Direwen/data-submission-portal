from django.core.management.base import BaseCommand
from entry_portal.models import DataEntry
import random

class Command(BaseCommand):
    help = 'Seeds the database with many DataEntry records.'

    def handle(self, *args, **kwargs):
        # Number of records to create
        num_records = 100

        # List to hold the DataEntry instances
        data_entries = []

        for i in range(num_records):
            # Randomly choose a category
            category = random.choice([DataEntry.TEXT_CATEGORY, DataEntry.IMAGE_CATEGORY])

            # Create a DataEntry instance
            data_entry = DataEntry(
                content=f"Sample content {i}",
                category=category,
                is_reviewed=random.choice([True, False])
            )
            data_entries.append(data_entry)

        # Use bulk_create to insert all records at once
        DataEntry.objects.bulk_create(data_entries)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {num_records} DataEntry records.'))