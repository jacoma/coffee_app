import csv
from django.core.management import BaseCommand

# Import the model 
from coffee.models import ratings
from django.contrib.auth.models import User


ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""

my_user = User.objects.get(username='jacoma')

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from children.csv"

    def handle(self, *args, **options):
            
        # Show this before loading the data into the database
        print("Loading data")


        #Code to load the data into database
        for row in csv.reader(open('./myratings.csv')):
            roaster=ratings(
                coffee_id=row[0],
                brew_method=row[1],
                reaction=row[2],
                rating=row[3],
                user_id=my_user)  


            roaster.save()