
#Full path and name to your csv file 
csv_filepathname="C:\\Users\\jacoma\\source\\repos\\coffee_app\\roast.csv" 

import csv
from django.core.management import BaseCommand

# Import the model 
from coffee.models import countries


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from children.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if countries.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading childrens data")


        #Code to load the data into database
        for row in csv.reader(open('./countries.csv')):
            roaster=countries(
                country_code=row[0],
                name=row[1],
                country_code_alpha=row[2],
                country_code_alpha3=row[3],
                name_long=row[4],
                latitude=row[5],
                longitude=row[5]
                )  
            roaster.save()