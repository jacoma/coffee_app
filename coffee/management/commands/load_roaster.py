import csv
from django.core.management import BaseCommand

# Import the model 
from coffee.models import *

from endpoints.ml.postgres_data import get_postgres_data
roasters = get_postgres_data('SELECT * FROM coffee_dim_roaster')


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

        # roasters = dim_roaster.objects.all().values_list('roaster_id', flat=True).distinct() 
        roast_id = roasters.roaster_id.unique()   

        #Code to load the data into database
        for row in csv.reader(open('endpoints\my_coffee\data\/new_roasters.csv')):
            
            if int(row[0]) in roast_id:            
                r = dim_roaster.objects.get(roaster_id=row[0])
                
                r.website = row[2]
                r.save(update_fields=['website'])
            else:
                # r=dim_roaster(roaster_id=row[0], name=row[1], website=row[2])
                # r.save() 
                print('no item')