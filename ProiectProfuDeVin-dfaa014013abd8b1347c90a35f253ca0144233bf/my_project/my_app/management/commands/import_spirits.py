import pandas as pd
from django.core.management.base import BaseCommand
from my_app.models import Spirits

class Command(BaseCommand):
    help = 'Populate the Spirits database from an Excel file'

    def handle(self, *args, **kwargs):
        # Path to the Excel file
        file_path =  'C:\\Users\\Patri\\AN2_sem1\\DB\\spirits.xlsx'

        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)
        df['Style'].fillna('-', inplace=True)

        # Loop through the rows and create Spirits entries
        for _, row in df.iterrows():
            spirit = Spirits(
                Type=row['Type'],
                Name=row['Name'],
                Style=row['Style'],
                AlcLvl=row['AlcLvl'],
                Price=row['Price'],
                Qty=row['Qty']
            )
            spirit.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the Spirits database'))
