import pandas as pd
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Reads data from an Excel file and writes it to a text file in SQL insert format'

    def handle(self, *args, **kwargs):
        excel_file = r'D:\ProiectProfuDeVin\my_project\my_app\management\commands\players.xlsx'
        txt_file = r'D:\ProiectProfuDeVin\my_project\my_app\management\commands\players.txt'
        self.read_excel_and_write_to_txt(excel_file, txt_file)

    def read_excel_and_write_to_txt(self, excel_file, txt_file):
        # Read the Excel file
        df = pd.read_excel(excel_file)

        # Open the text file for writing with UTF-8 encoding
        with open(txt_file, 'w', encoding='utf-8') as file:
            for index, row in df.iterrows():
                # Format the data into the desired SQL insert statement
                sql_insert = (
                    f"INSERT INTO PLAYERS (NAME,TEAM,AGE,RATING,ROLE,WORLD_RANK) VALUES "
                    f"('{row['NAME']}','{row['TEAM']}',{row['AGE']},{row['RATING']},'{row['ROLE']}',{row['WORLD_RANK']}');\n"
                )
                # Write the SQL insert statement to the text file
                file.write(sql_insert)