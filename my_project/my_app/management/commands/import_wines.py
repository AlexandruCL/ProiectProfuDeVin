import os
import pandas as pd
from django.core.management.base import BaseCommand
from my_app.models import Wines
from django.core.files import File
from django.conf import settings

class Command(BaseCommand):
    help = 'Populate the Spirits database from an Excel file'

    def handle(self, *args, **kwargs):
        # Path to the Excel file
        file_path =  'D:\\ProiectProfuDeVin\\Wine_list.xlsx'

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)

        df['Year'] = df['Year'].fillna(0)  # Fill with 0 if year is missing
        df['Grapes'] = df['Grapes'].fillna(' ')
        df['Region'] = df['Region'].fillna(' ')
        

        # Loop through the rows and create Spirits entries
        for _, row in df.iterrows():
            wine = Wines(
                Name = row['Name'],
                Type = row['Type'],
                Year = row['Year'],
                Grapes = row['Grapes'],
                Country = row['Country'],
                Region = row['Region'],
                Price = row['Price'],
                Description = row['Description'],
                Qty = row['Qty']

            )
            if isinstance(row['image'], str) and row['image']:
                    image_path = os.path.join(settings.MEDIA_ROOT, row['image'])
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as img_file:
                            wine.image.save(os.path.basename(image_path), File(img_file), save=False)

            wine.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the Wine database'))
