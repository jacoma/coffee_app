
#Full path and name to your csv file 
csv_filepathname="C:\\Users\\jacoma\\source\\repos\\coffee_app\\roast.csv" 

import csv
import re
import pandas as pd
from textblob import TextBlob
from django.core.management import BaseCommand

# Import the model 
from coffee.models import dim_notes

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
        # if dim_coffee.objects.exists():
        #     print('child data already loaded...exiting.')
        #     print(ALREDY_LOADED_ERROR_MESSAGE)
        #     return
            
        # Show this before loading the data into the database
        print("Loading data")

        #Code to load the data into database
        clean_words = [] 
    
        for row in csv.reader(open('endpoints\my_coffee\data\/new_notes.csv')):
            # To Lower
            words_lower = row[0].lower()
            
            # Replace 'and' with &
            words_replace = re.sub("\sand\s", "&", words_lower)
            words_replace = words_lower.replace("jamminess", "jam")
            
            # Split by comma
            tokens = re.split("[&,]", words_replace)
            
            # Clean whitespace
            tokens_strip = [x.strip(' ') for x in tokens]
            
            # Singular
            non_singular = ['molasses', 'nibs', 'bears', 'lemongrass', 'sweetness', 'citrus', 'narcissus', 'gummies']
            for t in tokens_strip:
                if t.__contains__('rries'):
                    t = t.replace('rries', 'rry')
                
                clean_words.append(t)

        final_words = pd.Series(clean_words).drop_duplicates().tolist()

        print(len(final_words) < len(clean_words))

        for i in range(0, len(final_words)):
            note=dim_notes(flavor_notes=final_words[i])
            note.save()