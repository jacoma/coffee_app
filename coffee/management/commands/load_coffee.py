
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

                r.tradeUrl = row[8]
                r.storage_path = row[7]

                r.save(update_fields=['tradeUrl', 'storage_path'])
            else:
            
                my_variety = row[6].split(", ")
                my_notes = row[11].split(", ")
                roaster_x=dim_roaster.objects.get(roaster_id=int(row[9]))
                varietals_x=dim_varietal.objects.filter(varietal__in=my_variety)
                notes_x=dim_notes.objects.filter(flavor_notes__in=my_notes)

                if row[3] == '':
                    elevation_x = 0
                evelvation_x = int(row[3])

                coffee=dim_coffee(
                    coffee_id=int(row[0]),
                    name=row[1],
                    roaster=roaster_x,
                    farmer=row[3],
                    process=row[6],
                    elevation=evelvation_x,
                    storage_path=row[7],
                    tradeUrl=row[8]
                    )  

                if row[10] == '':
                    print('')
                else:
                    coffee.country=countries.objects.get(country_code=int(row[10]))


                coffee.save()
                coffee.varietals.set(varietals_x)
                coffee.roaster_notes.set(notes_x)

                count+=1

                print(count, "completed")