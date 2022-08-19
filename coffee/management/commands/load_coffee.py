
import csv
from django.core.management import BaseCommand

# Import the model 
from coffee.models import *

from endpoints.ml.postgres_data import get_postgres_data
coffees = get_postgres_data('SELECT * FROM coffee_dim_coffee')


ALREADY_LOADED_ERROR_MESSAGE = """
LOADED
"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from the cleaned trade coffee."

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        # if dim_coffee.objects.exists():
        #     print('coffee data already loaded...')
        #     print(ALREADY_LOADED_ERROR_MESSAGE)
        #     return
            
        # Show this before loading the data into the database
        print("Loading data")

        coffee_ids = coffees.coffee_id.unique()

        count = 0
        #Code to load the data into database
        for row in csv.reader(open('endpoints\\data\\tmp\\final_coffee.csv', encoding='cp437')):
         
            print(row[0])
            if int(row[0]) in coffee_ids:     
                pass       
                # r = dim_coffee.objects.get(coffee_id=int(row[0]))

                # r.tradeUrl = row[8]
                # r.storage_path = row[7]

                # r.save(update_fields=['tradeUrl', 'storage_path'])
            else:
            
                print("Get variety")
                my_variety = row[7].split(", ")

                print("Get notes")
                my_notes = row[15].split(", ")

                print("Match roaster")
                roaster_x=dim_roaster.objects.get(roaster_id=int(row[11]))

                print("Match variety")
                varietals_x=dim_varietal.objects.filter(varietal__in=my_variety)

                print("Match notes")
                notes_x=dim_notes.objects.filter(flavor_notes__in=my_notes)

                print("Get elevation")
                if row[6] == '':
                    elevation_x = 0
                elevation_x = int(row[6])

                print("Create coffee")
                coffee=dim_coffee(
                    coffee_id=int(row[0]),
                    name=row[1],
                    roaster=roaster_x,
                    farmer=row[5],
                    process=row[2],
                    elevation=elevation_x,
                    storage_path=row[9],
                    tradeUrl=row[8]
                    )  

                if row[3] == '':
                    print('')
                else:
                    coffee.country=countries.objects.get(country_code=int(row[3]))

                coffee.save()
                coffee.varietals.set(varietals_x)
                coffee.roaster_notes.set(notes_x)

                count+=1

                print(count, "completed")