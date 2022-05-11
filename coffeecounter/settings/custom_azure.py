from storages.backends.azure_storage import AzureStorage
import os

class AzureStaticStorage(AzureStorage):
    account_name = os.getenv('AZ_STORAGE_NAME', '') # Must be replaced by your <storage_account_name>
    account_key = os.getenv('AZ_STORAGE_KEY', '') # Must be replaced by your <storage_account_key>
    azure_container = os.getenv('AZ_STATIC_CONTAINER', '')
    expiration_secs = None