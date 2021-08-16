
#Full path and name to your csv file 
csv_filepathname="C:\\Users\\jacoma\\source\\repos\\coffee_app\\roast.csv" 

import csv
from django.core.management import BaseCommand

# Import the model 
from coffee.models import dim_coffee


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
        if dim_coffee.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading childrens data")


        #Code to load the data into database
        for row in csv.reader(open('./test_coffee.csv')):
            roaster=dim_coffee(
                coffee_id=row[0],
                name=row[1],
                roaster=row[2],
                farmer=row[3],
                country=row[4],
                varietals=row[5],
                process=row[6],
                elevation=row[7],
                roaster_notes=row[8])  


            roaster.save()