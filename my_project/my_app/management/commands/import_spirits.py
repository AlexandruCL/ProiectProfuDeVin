import os
import pandas as pd
from django.core.management.base import BaseCommand
from my_app.models import Spirits
from django.core.files import File
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the Spirits database from an Excel file'

    def handle(self, *args, **kwargs):
        # Path to the Excel file
        file_path =  'D:\\ProiectProfuDeVin\\spirits.xlsx'

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        df['Style'] = df['Style'].fillna(' ')

        # Loop through the rows and create Spirits entries
        for _, row in df.iterrows():
            style = row['Style'] if row['Style'] != ' ' else None

            spirit = Spirits(
                Type=row['Type'],
                Name=row['Name'],
                Style=style,
                AlcLvl=row['AlcLvl'],
                Price=row['Price'],
                Qty=row['Qty']
            )
            if isinstance(row['image'], str) and row['image']:
                    image_path = os.path.join(settings.MEDIA_ROOT, row['image'])
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as img_file:
                            spirit.image.save(os.path.basename(image_path), File(img_file), save=False)
            spirit.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the Spirits database'))
