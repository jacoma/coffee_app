
import csv
from django.core.management import BaseCommand

# Import the model 
from coffee.models import *

from endpoints.ml.postgres_data import get_postgres_data
coffees = get_postgres_data('SELECT * FROM coffee_dim_coffee')


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

        coffee_ids = coffees.coffee_id.unique()

        count = 0
        #Code to load the data into database
        for row in csv.reader(open('endpoints\my_coffee\data\/final_trade_coffee.csv', encoding='cp437')):
         
            if int(row[0]) in coffee_ids:            
                r = dim_coffee.objects.get(coffee_id=int(row[0]))
                # my_variety = row[6].split(",")
                # my_notes = row[11].split(",")

                # varietals_x=dim_varietal.objects.filter(varietal__in=my_variety)
                # notes_x=dim_notes.objects.filter(flavor_notes__in=my_notes)

                # r.varietals.set(varietals_x)
                # r.roaster_notes.set(notes_x)

                # if row[3] == '':
                #     r.elevation_x = 0
                # r.elevation = int(row[3])

                # r.farmer = row[4]
                # r.process = row[5]

                r.storage_path = '.'.join([row[7], 'jpg'])

                r.save(update_fields=['storage_path'])
            else:
                print('no item')
            
            count+=1

            print(count, "completed")