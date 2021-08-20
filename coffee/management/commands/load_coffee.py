
#Full path and name to your csv file 
csv_filepathname="C:\\Users\\jacoma\\source\\repos\\coffee_app\\roast.csv" 

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
    help = "Loads data from children.csv"

    def handle(self, *args, **options):
    
        # # Show this if the data already exist in the database
        # if dim_coffee.objects.exists():
        #     print('child data already loaded...exiting.')
        #     print(ALREDY_LOADED_ERROR_MESSAGE)
        #     return
            
        # Show this before loading the data into the database
        print("Loading data")


        #Code to load the data into database
        for row in csv.reader(open('./mycoffee.csv')):
            my_variety = row[5].split(", ")
            my_notes = row[8].split(", ")
            roaster_x=dim_roaster.objects.get(roaster_id=row[2])
            country_x=countries.objects.get(country_code=row[4])
            varietals_x=dim_varietal.objects.filter(varietal__in=my_variety)
            notes_x=dim_notes.objects.filter(flavor_notes__in=my_notes)

            if row[7] == '':
                elevation_x = 0
            evelvation_x = row[7]

            coffee=dim_coffee(
                coffee_id=row[0],
                name=row[1],
                roaster=roaster_x,
                farmer=row[3],
                country=country_x,
                process=row[6],
                elevation=evelvation_x)  

            coffee.save()
            coffee.varietals.set(varietals_x)
            coffee.roaster_notes.set(notes_x)