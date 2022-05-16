import numpy as np
import pandas as pd
from azure.storage.blob import BlockBlobService
from io import StringIO
import re
from pyparsing import LRUMemo
from textblob import TextBlob
from endpoints.ml.postgres_data import get_postgres_data

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
def get_coffee_info():
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
    
    return coffee_info

trade_df = get_coffee_info()

trade_df.rename(columns={'variety':'varietals'}, inplace=True)


##****** PROCESS VARIETALS ******##
special_characters = [' and ',' & ',', ',' / ', '/', ' | ']

def get_clean_varietals(row):

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
                new_word = word.capitalize()
                word_list.append(new_word)
            
            new_var = " ".join(word_list)
        else:
            new_var = var.capitalize()

        cleaned_vars.append(new_var)

    new_varietals = ",".join(cleaned_vars)
    
    return new_varietals

trade_df['varietals'] = trade_df.apply(lambda row: get_clean_varietals(row), axis = 1)



##****** PROCESS ELEVATION ******##
def get_cleaned_elevation(row):
    temp = row.elevation.replace(',', '').split(' - ')

    temp = [int(t) for t in temp]

    elevation = np.average(temp)

    return int(elevation)

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
for i in range(0, len(roaster_df)):

    if np.isnan(roaster_df.roaster_id[i]):
        roaster_df.roaster_id[i]=np.max(roasters.roaster_id)+i
    
    roaster_df.roaster_id[i]=roaster_df.roaster_id[i].astype(int)
    
    roaster_df.website[i]=roaster_df.roaster_url[i]

## Merge updated roaster information with trade coffee dataframe.
trade_df1 = pd.merge(trade_df, roaster_df, how='left', left_on='cleaned_roaster', right_on='cleaned_roaster')
trade_df1.drop(['name_y', 'roaster_url_y', 'roaster_url_x', 'roaster'], inplace=True, axis=1)
trade_df1.rename(columns={'name_x':'name', 'cleaned_roaster':'roaster'}, inplace=True)

##****** PROCESS COFFEE_ID ******##
coffees = get_postgres_data('SELECT * FROM coffee_dim_coffee')

coffees['lower_name'] = [str(name).lower() for name in coffees.name]
trade_df1['lower_name'] = [str(name).lower() for name in trade_df1.name]

merged_temp = pd.merge(
    trade_df1, 
    coffees, 
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
def get_updated_process(process):
    """Function to return a cleaned process type. If not found, the original value is returned."""

    switch={
       'Natural/Dry Processed': "Natural",
       'Pulped Natural/Honey': "Honey",
       'Experimental/Other': "Experimental"
       }
    return switch.get(process, process)

for i in range(0, len(new_coffee)):
    item = str(new_coffee.process[i])
    split_item = item.split(",")[0]

    new_coffee.process[i] = get_updated_process(split_item)


##****** PROCESS NOTES ******##
import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

tokenizer = RegexpTokenizer(r'\w+')
lemmatizer = WordNetLemmatizer()

for i in range(0, len(new_coffee)):
    if type(new_coffee.loc[i, 'roaster_notes'])==float:
        new_coffee.loc[i, 'roaster_notes']=''   

new_coffee['all_notes'] = new_coffee['other_notes']+' '+(new_coffee['roaster_notes'])

notes_3 = all_notes.Note_3

temp_df=pd.DataFrame(columns=['product_id', 'notes_list'])
for i in range(0,len(new_coffee)):
    print(i)

    notes_list = []

    tokens = tokenizer.tokenize(new_coffee.loc[i, 'all_notes'])
    filtered_tokens = [t.lower() for t in tokens if not t in stopwords.words("english")]
    lem_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    token_list = []
    for token in lem_tokens:
        result = list(words_in_string(notes_3, token))

        if len(result) > 0:
            token_list.append(result)

    combined_text = ' '.join(lem_tokens)
    ngram_object = TextBlob(combined_text)
    ngrams = ngram_object.ngrams(n=2) # Computing Bigrams

    for ngram in ngrams:
        text = ' '.join(ngram)
        result = list(words_in_string(notes_3, text))

        if len(result) > 0:
            token_list.append(result)

    for t in token_list:
        notes_list.extend(t)

    notes_set = set(notes_list)
    
    new_row = {'product_id': new_coffee.product_id[i], 'notes_list':",".join(notes_set)}
    
    temp_df = temp_df.append(new_row, ignore_index=True)

trade_notes_df = pd.merge(new_coffee, temp_df, how='inner', on='product_id')

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

trade_notes_df['coffee_id'] = [get_new_id(coffee_id_list) for i in range(0, len(trade_notes_df))]

columns = ["name", "process", "subregion","farmer", "elevation", "varietals", "trade_link", "storage_path", "roaster", "roaster_id", "website",	"coffee_id", "product_id", "country_id",	"all_notes", "notes_list"]
trade_notes_df[columns].to_csv('endpoints/data/tmp/cleaned_trade_coffee.csv', index=False)


coffees = get_postgres_data(
    'SELECT * FROM coffee_dim_coffee dc LEFT JOIN coffee_dim_coffee_varietals dcv ON dc.coffee_id = dcv.dim_coffee_id')

