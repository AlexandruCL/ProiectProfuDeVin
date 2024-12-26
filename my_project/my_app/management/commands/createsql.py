import pandas as pd
from django.core.management.base import BaseCommand

# Path to the Excel files
spirits_file_path = 'D:\\ProiectProfuDeVin\\spirits.xlsx'
wines_file_path = 'D:\\ProiectProfuDeVin\\Wine_list.xlsx'

# Read the Excel files into pandas DataFrames
spirits_df = pd.read_excel(spirits_file_path)
wines_df = pd.read_excel(wines_file_path)

# Fill missing values
spirits_df['Style'] = spirits_df['Style'].fillna(' ')
wines_df['Year'] = wines_df['Year'].fillna(0)
wines_df['Grapes'] = wines_df['Grapes'].fillna(' ')
wines_df['Region'] = wines_df['Region'].fillna(' ')

# Function to escape single quotes in strings
def escape_single_quotes(value):
    if isinstance(value, str):
        value = value.replace("'", "''")
    return value

class Command(BaseCommand):
    help = 'Reads data from Excel files and writes it to a SQL file'

    def handle(self, *args, **kwargs):
        # Generate SQL script for spirits
        spirits_sql = ""
        spirits_sql = "DELETE from my_app_spirits;\n"
        for _, row in spirits_df.iterrows():
            style = escape_single_quotes(row['Style']) if row['Style'] != ' ' else None
            image = escape_single_quotes(row['image']) if isinstance(row['image'], str) and row['image'] else None
            spirits_sql += f"INSERT INTO my_app_spirits (Type, Name, Style, AlcLvl, Price, Qty, image) VALUES ('{escape_single_quotes(row['Type'])}', '{escape_single_quotes(row['Name'])}', '{style}', {row['AlcLvl']}, {row['Price']}, {row['Qty']}, '{image}');\n"

        # Generate SQL script for wines
        wines_sql = ""
        wines_sql = "DELETE from my_app_wines;\n"
        for _, row in wines_df.iterrows():
            year = int(row['Year']) if row['Year'] != 0 else 0
            grapes = escape_single_quotes(row['Grapes']) if row['Grapes'] != ' ' else None
            region = escape_single_quotes(row['Region']) if row['Region'] != ' ' else None
            image = escape_single_quotes(row['image']) if isinstance(row['image'], str) and row['image'] else None
            wines_sql += f"INSERT INTO my_app_wines (Name, Type, Year, Grapes, Country, Region, Price, Description, Qty, image) VALUES ('{escape_single_quotes(row['Name'])}', '{escape_single_quotes(row['Type'])}', {year}, '{grapes}', '{escape_single_quotes(row['Country'])}', '{region}', {row['Price']}, '{escape_single_quotes(row['Description'])}', {row['Qty']}, '{image}');\n"

        # Write the SQL script to a file with UTF-8 encoding
        try:
            with open('D:\\ProiectProfuDeVin\\my_project\\my_app\\management\\commands\\populate_tables.sql', 'w', encoding='utf-8') as file:
                file.write(spirits_sql)
                file.write('\n')
                file.write(wines_sql)
            print("File written successfully.")
        except Exception as e:
            print(f"Error writing to file: {e}")