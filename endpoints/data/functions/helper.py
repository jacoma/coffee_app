import pandas as pd
from azure.storage.blob import BlockBlobService
from io import StringIO
from dotenv import dotenv_values
config = dotenv_values(".env")

def get_data(csv_path, adls_path):
    try:
        data = pd.read_csv(csv_path)

        print("Found local file")
    except:
        blob_service = BlockBlobService( 
            account_name=config['AZ_STORAGE_NAME'], 
            account_key=config['AZ_ACCOUNT_KEY'])

        blob_string = blob_service.get_blob_to_text(
            config['AZ_COFFEE_CONTAINER'], 
            adls_path
            )
        data = pd.read_csv(StringIO(blob_string.content))

        print("Found ADLS file")
    
    return data