import os
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand
from my_app.models import Wines
from django.core.files import File
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the Spirits database from an Excel file'

    def add_arguments(self, parser):
        repo_root = Path(settings.BASE_DIR).resolve().parent
        parser.add_argument(
            '--file',
            dest='file_path',
            default=str(repo_root / 'Wine_list.xlsx'),
            help='Path to the Wine_list.xlsx file (defaults to repo root).',
        )
        parser.add_argument(
            '--overwrite-images',
            action='store_true',
            help='Overwrite image field even if already set.',
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        overwrite_images = kwargs['overwrite_images']

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Excel file not found: {file_path}. "
                "Commit it into the repo or pass --file /path/to/Wine_list.xlsx"
            )

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)

        df['Year'] = df['Year'].fillna(0)  # Fill with 0 if year is missing
        df['Grapes'] = df['Grapes'].fillna(' ')
        df['Region'] = df['Region'].fillna(' ')

        # Loop through the rows and create/update Wines entries
        for _, row in df.iterrows():
            region = row['Region'] if row['Region'] != ' ' else None
            grapes = row['Grapes'] if row['Grapes'] != ' ' else None

            wine, created = Wines.objects.update_or_create(
                Name=row['Name'],
                Type=row['Type'],
                Year=row['Year'],
                Country=row['Country'],
                defaults={
                    'Grapes': grapes,
                    'Region': region,
                    'Price': row['Price'],
                    'Description': row['Description'],
                    'Qty': row['Qty'],
                },
            )

            image_value = row.get('image') if hasattr(row, 'get') else row['image']
            if isinstance(image_value, str) and image_value:
                if overwrite_images or not wine.image:
                    image_path = os.path.join(settings.MEDIA_ROOT, image_value)
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as img_file:
                            wine.image.save(os.path.basename(image_path), File(img_file), save=True)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Wine database'))