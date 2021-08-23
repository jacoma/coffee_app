import csv
from django.core.management import BaseCommand

# Import the model 
from coffee.models import countries


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from countries"

    def handle(self, *args, **options):
           
        # Show this before loading the data into the database
        print("updating")

        #Code to load the data into database
        for row in csv.reader(open('C:/Users/jacoma/OneDrive - Microsoft/Desktop/data/countries.csv')):
            country=countries.objects.get(country_code=row[0])
            country.region = row[7]
            country.subregion = row[8]
            country.save(update_fields=['region', 'subregion'])
            print(row[0])