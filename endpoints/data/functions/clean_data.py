import numpy as np
import pandas as pd
from azure.storage.blob import BlockBlobService
from io import StringIO
import re

from dotenv import dotenv_values
config = dotenv_values(".env")

def get_coffee_info():
    """Get CSV file. First, look in the local file directory. If not found, look in the Azure storage location. Also, if there is an "Unnamed" column in the CSV, drop.
    """
    try:
        coffee_info = pd.read_csv('endpoints\\data\\tmp\\coffee_pages.csv')

        print("Found local file")
    except:
        blob_service = BlockBlobService( 
            account_name=config['AZ_STORAGE_NAME'], 
            account_key=config['AZ_ACCOUNT_KEY'])

        blob_string = blob_service.get_blob_to_text('coffeecontainer', 'ml/recommendations/data/coffee_info.csv')
        coffee_info = pd.read_csv(StringIO(blob_string.content))

        print("Found ADLS file")

    if 'Unnamed' in coffee_info.columns[0]:
        coffee_info.drop(coffee_info.columns[0], axis=1, inplace=True)

    coffee_info = coffee_info[~((coffee_info.name.isnull()) & ( coffee_info.roaster.isnull()))]

    if 'variety' in coffee_info.columns:
        coffee_info.rename(columns={'variety':'varietals'}, inplace=True)
    
    return coffee_info

##***** get_clean_varietals *****##
special_characters = [' and ',' & ',', ',' / ', '/', ' | ']

def get_clean_varietals(row):
    """Clean the raw text data, for varietals, extracted from the Trade website, including:
    - Replacing nan with empty strings.
    - Stripping white space,
    - Capitalization
    - Replacing special characters
    - Splitting the text string into individual varietal values, then creating into a list.
    #NEED TO UPDATE
    - Replace wolicho, 
    - Fuzzy match listed varietals with official varietal names
    - Add new varietals to a list which can be uploaded to the database.

    Args:
        row (_type_): _description_

    Returns:
        list: list of string varietal values
    """
    if type(row.varietals)==float:
        row.varietals=''

    if row.varietals=='nan':
        row.varietals=''

    row.varietals = row.varietals.strip().capitalize()
    for c in special_characters:
        row.varietals = row.varietals.replace(c, ',')

    row.varietals = row.varietals.replace('-', '')
    row.varietals = row.varietals.replace('.', '')

    vars = row.varietals.split(",")
        
    cleaned_vars=[]
    for var in vars:

        if var.count(' ') > 0:
            words = var.split(" ")

            word_list = []
            for word in words:
                if re.match('\([a-zA-Z]*\)', word):
                    pass
                else:
                    new_word = word.capitalize()
                    word_list.append(new_word)
            
            new_var = " ".join(word_list)
        else:
            new_var = var.capitalize()

        if re.match('sl\d\d', new_var, re.I):
            new_var = new_var.upper()

        cleaned_vars.append(new_var)

    new_varietals = ",".join(cleaned_vars)
    
    return new_varietals


##***** get_cleaned_elevation *****##
def get_cleaned_elevation(row):
    """Cleans the raw elevation text/data extracted from the Trade webiste. This includes replacing commas with a space and splitting the text by "-". If there are two elevation values, the average is found.

    Args:
        row (_type_): _description_

    Returns:
        int: cleaned elevation value
    """
    temp = row.elevation.replace(',', '').split(' - ')

    temp = [int(t) for t in temp]

    elevation = np.average(temp)

    return int(elevation)



##***** get_cleaned_notes *****##
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import pos_tag, word_tokenize
# import nltk
# nltk.download('averaged_perceptron_tagger')

lemmatizer = WordNetLemmatizer()

def pos_tagger(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:         
            return None

def get_lemma_tokens(notes_column):

    pos_tagged = pos_tag(word_tokenize(notes_column))
    
    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged))

    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            # if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:       
            # else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    lemmatized_sentence = " ".join(lemmatized_sentence)
