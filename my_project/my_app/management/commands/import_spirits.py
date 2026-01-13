import os
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand
from my_app.models import Spirits
from django.core.files import File
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the Spirits database from an Excel file'

    def add_arguments(self, parser):
        repo_root = Path(settings.BASE_DIR).resolve().parent
        parser.add_argument(
            '--file',
            dest='file_path',
            default=str(repo_root / 'spirits.xlsx'),
            help='Path to the spirits.xlsx file (defaults to repo root).',
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
                "Commit it into the repo or pass --file /path/to/spirits.xlsx"
            )

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        df['Style'] = df['Style'].fillna(' ')

        # Loop through the rows and create/update Spirits entries
        for _, row in df.iterrows():
            style = row['Style'] if row['Style'] != ' ' else None

            spirit, created = Spirits.objects.update_or_create(
                Type=row['Type'],
                Name=row['Name'],
                defaults={
                    'Style': style,
                    'AlcLvl': row['AlcLvl'],
                    'Price': row['Price'],
                    'Qty': row['Qty'],
                },
            )

            image_value = row.get('image') if hasattr(row, 'get') else row['image']
            if isinstance(image_value, str) and image_value:
                if overwrite_images or not spirit.image:
                    image_path = os.path.join(settings.MEDIA_ROOT, image_value)
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as img_file:
                            spirit.image.save(os.path.basename(image_path), File(img_file), save=True)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Spirits database'))
