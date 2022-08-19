import numpy as np
import pandas as pd
from azure.storage.blob import BlockBlobService
from io import StringIO
import re
from pyparsing import LRUMemo
from textblob import TextBlob
from endpoints.ml.postgres_data import get_postgres_data, create_postgres_data
from endpoints.data.functions.clean_data import get_coffee_info, get_clean_varietals, get_cleaned_elevation, get_lemma_tokens
import psycopg2

from dotenv import dotenv_values
config = dotenv_values(".env")

##****** DEFINE FUNCTIONS ******##
def words_in_string(word_list, a_string):
    '''Returns unique elements found in both lists'''
    my_list = [] 
    split_list = a_string.split()
    for elem in split_list:
        my_list.append(elem)
    my_list.append(a_string)
    return set(word_list).intersection(my_list)


##****** LOAD DATA ******##
blob_service = BlockBlobService( 
            account_name=config['AZ_STORAGE_NAME'], 
            account_key=config['AZ_ACCOUNT_KEY'])

# Notes Wheel
blob_string = blob_service.get_blob_to_text('coffeecontainer', 'notes_wheel.csv')
all_notes = pd.read_csv(StringIO(blob_string.content))

# Coffee Info
trade_df = get_coffee_info()

##****** PROCESS VARIETALS ******##
trade_df['varietals'] = trade_df.apply(lambda row: get_clean_varietals(row), axis = 1)

## New varietal types
db_varietals = get_postgres_data('SELECT * FROM coffee_dim_varietal')

new_varietals = pd.read_csv('endpoints\\data\\tmp\\new_varietals.csv', header=None)

new_varietal_types = pd.DataFrame(set.difference(set(new_varietals[0]), set(db_varietals.varietal)), columns=['varietal'])

max_id = np.max(db_varietals.id)

new_varietal_types['new_id'] = new_varietal_types.apply(lambda row: max_id + row.name + 1, axis=1)

def upload_new_varietal(row, cursor):

    query = "INSERT INTO coffee_dim_varietal (id, varietal) VALUES (%s, %s)"
    values = (int(row.new_id), row.varietal)

    cursor.execute(query, values)

    conn.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into table")


# Set up a connection to the postgres server.
conn_string = "host="+ (config["DATABASE_HOST"] or None) +" port="+ "5432" +" dbname="+ (config["DATABASE_NAME"] or None) +" user=" + (config["DATABASE_USER"] or None) \
+" password="+ (config["DATABASE_PASS"] or None) +" sslmode=require"

conn=psycopg2.connect(conn_string)

# Create a cursor object
cursor = conn.cursor()

new_varietal_types.apply(lambda row: upload_new_varietal(row, cursor), axis = 1)

cursor.close()

##****** PROCESS ELEVATION ******##
trade_df['elevation'] = trade_df.apply(lambda row: get_cleaned_elevation(row), axis = 1)

trade_df.drop_duplicates(inplace=True)

##****** PROCESS ROASTER ******##
roasters = get_postgres_data('SELECT * FROM coffee_dim_roaster')

# Update the values for some of the roasters and save as "cleaned_roaster"
trade_df['cleaned_roaster'] = np.select(
    [
        trade_df.roaster=='Alma',
        trade_df.roaster=='Anodyne',
        trade_df.roaster=='Mother Tongue',
        trade_df.roaster=='Blueprint',
        trade_df.roaster=='Joe',
        trade_df.roaster=='Madcap',
        trade_df.roaster=="PT's",
        trade_df.roaster=='ReAnimator',
        trade_df.roaster=='Sightglass',
        trade_df.roaster=='Sterling'
    ], 
    [
        'Alma Coffee',
        'Anodyne Coffee Roasters',
        'Mother Tongue Coffee',
        'Blueprint Coffee Roasters',
        'Joe Coffee',
        'Mad Cap',
        "PT's Coffee Roasting Co.",
        "ReAnimator Coffee Roasters",
        "Sight Glass",
        "Sterling Coffee Roasters"
    ],
    default=trade_df.roaster)

## Distinct list of roasters
new_roasters=trade_df.loc[:, ('cleaned_roaster','roaster_url')].drop_duplicates()

# Merge existing list of roasters in the database with the unique list from the new trade CSV.
roaster_df = pd.merge(new_roasters, roasters, how='left', left_on='cleaned_roaster', right_on='name')

## Replace information if the roaster exists
roaster_df['roaster_id_new'] = roaster_df.apply(lambda row: (np.max(roasters.roaster_id)+row.name+1).astype(int) if np.isnan(row.roaster_id) else row.roaster_id, axis=1)
    
roaster_df['website']=roaster_df.roaster_url

## New roasters - add to database
def upload_new_roaster(row, cursor):

    query = "INSERT INTO coffee_dim_roaster (roaster_id, name, website) VALUES (%s, %s, %s)"
    values = (int(row.roaster_id_new), row.cleaned_roaster, row.website)

    cursor.execute(query, values)

    conn.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into table")


# Set up a connection to the postgres server.
conn=psycopg2.connect(conn_string)

# Create a cursor object
cursor = conn.cursor()

roaster_df[np.isnan(roaster_df.roaster_id)].apply(lambda row: upload_new_roaster(row, cursor), axis = 1)

cursor.close()


## Merge updated roaster information with trade coffee dataframe.
trade_df1 = pd.merge(trade_df, roaster_df, how='left', left_on='cleaned_roaster', right_on='cleaned_roaster')
trade_df1.drop(['name_y', 'roaster_url_y', 'roaster_url_x', 'roaster'], inplace=True, axis=1)
trade_df1.rename(columns={'name_x':'name', 'cleaned_roaster':'roaster'}, inplace=True)

##****** PROCESS COFFEE_ID ******##
db_coffees = get_postgres_data('SELECT * FROM coffee_dim_coffee')

db_coffees['lower_name'] = [str(name).lower() for name in db_coffees.name]
trade_df1['lower_name'] = [str(name).lower() for name in trade_df1.name]

merged_temp = pd.merge(
    trade_df1, 
    db_coffees, 
    how='left', 
    on=['lower_name', 'roaster_id'], 
    suffixes=['_trade', '_app'])

# Coalesce columns
cols = ['name', 'elevation', 'farmer', 'process', 'storage_path']
for col in cols:
    merged_temp[col] = ''

    trade = col+'_trade'
    app = col+'_app'

    merged_temp[col] = merged_temp[[app, trade]].bfill(axis=1).iloc[:, 0]

merged_df = merged_temp[['product_id', 'coffee_id', 'name', 'roaster_id', 'roaster', 'elevation', 'farmer', 'process', 'country_id', 'subregion', 'varietals', 'roaster_notes', 'other_notes', 'image_url', 'trade_link', 'storage_path_trade', 'website']]

# Drop coffee without a name and roaster name.
new_coffee = merged_df[merged_df.coffee_id.isnull()]

new_coffee = new_coffee[~((new_coffee.name.isnull()) & (new_coffee.roaster.isnull()))].reset_index()

# Drop coffee with '5 lb' in the name.
new_coffee['delete_row'] = [str(row).find(' - 5 lb bag') for row in new_coffee['name']]

new_coffee = new_coffee[new_coffee['delete_row'] == -1].reset_index()

new_coffee.drop(['delete_row', 'index'], inplace=True, axis=1)

##****** PROCESS COFFEE PROCESS TYPE ******##
def clean_process(process):
    """Function to return a cleaned process type. If not found, the original value is returned."""

    switch={
       'Natural/Dry Processed': "Natural",
       'Pulped Natural/Honey': "Honey",
       'Experimental/Other': "Experimental"
       }
    return switch.get(process, process)

def get_split_update_process(row):
    item = str(row.process)
    split_item = item.split(",")[0]

    new_value = clean_process(split_item)

    return new_value

new_coffee['process'] = new_coffee.apply(lambda row: get_split_update_process(row), axis = 1)

## New process types
new_process_types = set.difference(set(new_coffee.process), set(db_coffees.process))



##****** PROCESS NOTES ******##
for i in range(0, len(new_coffee)):
    if type(new_coffee.loc[i, 'roaster_notes'])==float:
        new_coffee.loc[i, 'roaster_notes']=''

new_coffee['all_notes'] = new_coffee['other_notes']+' '+(new_coffee['roaster_notes'])

import spacy
nlp = spacy.load("en_core_web_sm")
nlp_token = spacy.load(r"C:\Users\jacoma\repos\coffee_app\endpoints\data\output\model-best") #load the best model

def get_notes_from_ner(row):
    doc = nlp(row['all_notes'])
    lemmatized_sentence = " ".join([token.lemma_ for token in doc])
    print(lemmatized_sentence)

    # lemmatized_sentence = get_lemma_tokens(row['all_notes'])

    doc_token = nlp_token(lemmatized_sentence)

    tasting_notes = set()
    for ent in doc_token.ents:
        if ent.label_ == 'tasting':
            word = ent.text
            word_lower = word.lower()

            tasting_notes.add(word_lower)            
    
    final_list = ",".join(tasting_notes)

    return final_list

new_coffee['notes_list'] = new_coffee.apply(lambda row: get_notes_from_ner(row), axis=1)

new_coffee.to_csv('endpoints/data/tmp/coffee_notes_06202022_2.csv', index=False)

## NEW NOTES
db_notes = get_postgres_data('SELECT * FROM coffee_dim_notes')

new_notes = pd.read_csv('endpoints\\data\\tmp\\new_notes.csv', header=None)

new_notes_types = pd.DataFrame(set.difference(set(new_notes[0]), set(db_notes.flavor_notes)), columns=['notes'])

max_id = np.max(db_notes.id)

new_notes_types['new_id'] = new_notes_types.apply(lambda row: max_id + row.name + 1, axis=1)

def upload_new_notes(row, cursor):

    query = "INSERT INTO coffee_dim_notes (id, flavor_notes) VALUES (%s, %s)"
    values = (int(row.new_id), row.notes)

    cursor.execute(query, values)

    conn.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into table")

# Set up a connection to the postgres server.
conn_string = "host="+ (config["DATABASE_HOST"] or None) +" port="+ "5432" +" dbname="+ (config["DATABASE_NAME"] or None) +" user=" + (config["DATABASE_USER"] or None) \
+" password="+ (config["DATABASE_PASS"] or None) +" sslmode=require"

conn=psycopg2.connect(conn_string)

# Create a cursor object
cursor = conn.cursor()

new_notes_types.apply(lambda row: upload_new_notes(row, cursor), axis = 1)

cursor.close()

###*** COUNTRY ***###
countries = get_postgres_data('SELECT * FROM coffee_countries')

countries = countries[["name", "country_code", "country_code_alpha"]]

# countries.to_csv('endpoints\\data\\tmp\\countries.csv', index=False)

new_coffee = pd.read_csv('endpoints\\data\\tmp\\cleaned_trade_coffee.csv', encoding='cp437')
new_coffee.columns = ["coffee_id", "name", "process", "country", "subregion","farmer", "elevation", "varietals", "trade_link", "storage_path_trade", "roaster", "roaster_id", "website", "product_id", "country_id","all_notes", "notes_list"]

new_coffee = pd.merge(new_coffee, countries, how = "left", left_on ="country", right_on="name")

new_coffee = new_coffee[["coffee_id", "name_x", "process", "country_code", "subregion","farmer", "elevation", "varietals", "trade_link", "storage_path_trade", "roaster", "roaster_id", "website", "product_id", "all_notes", "notes_list"]]

new_coffee.rename(columns={'name_x':'name'}, inplace=True)

new_coffee.to_csv('endpoints/data/tmp/final_coffee.csv', index=False)

###
# Add coffee_id that doesn't already exist in table.
###
import random
coffee_id_list = [int(id) for id in merged_temp[~merged_temp.coffee_id.isnull()].coffee_id.unique()]

def get_new_id(coffee_id_list):
    new_id = random.randint(1000,9998)

    while new_id in coffee_id_list:
        new_id = random.randint(1000,9998)
    
    return new_id

new_coffee['coffee_id'] = [get_new_id(coffee_id_list) for i in range(0, len(new_coffee))]

columns = ["name", "process", "subregion","farmer", "elevation", "varietals", "trade_link", "storage_path_trade", "roaster", "roaster_id", "website",	"coffee_id", "product_id", "country_id",	"all_notes", "notes_list"]
new_coffee[columns].to_csv('endpoints/data/tmp/cleaned_trade_coffee.csv', index=False)
