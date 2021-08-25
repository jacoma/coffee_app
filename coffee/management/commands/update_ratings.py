import csv
from django.core.management import BaseCommand

# Import the model 
from coffee.models import ratings


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from ratings"

    def handle(self, *args, **options):
           
        # Show this before loading the data into the database
        print("updating")

        #Code to load the data into database
        for row in csv.reader(open('C:/Users/jacoma/OneDrive - Microsoft/Desktop/data/coffee_ratings.csv')):
            rate=ratings.objects.get(rating_id=row[0])
            rate.rating_date = row[7]
            rate.save(update_fields=['rating_date'])
            print(row[0])