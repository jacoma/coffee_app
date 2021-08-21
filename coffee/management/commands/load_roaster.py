import csv
from django.core.management import BaseCommand

# Import the model 
from coffee.models import *


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from roast.csv"

    def handle(self, *args, **options):
    
        # Show this before loading the data into the database
        print("Loading roaster data")


        #Code to load the data into database
        for row in csv.reader(open('C:/Users/jacoma/OneDrive - Microsoft/Desktop/data/roast.csv')):
            roaster=dim_roaster(roaster_id=row[0], name=row[1])  
            roaster.save()