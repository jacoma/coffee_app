
#Full path and name to your csv file 
csv_filepathname="C:\\Users\\jacoma\\source\\repos\\coffee_app\\roast.csv" 

import csv
from django.core.management import BaseCommand

# Import the model 
from coffee.models import dim_roaster


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
        if dim_roaster.objects.exists():
            print('child data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading childrens data")


        #Code to load the data into database
        for row in csv.reader(open('./roast.csv')):
            roaster=dim_roaster(roaster_id=row[0], name=row[1])  
            roaster.save()