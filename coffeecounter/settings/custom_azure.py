from storages.backends.azure_storage import AzureStorage
import os

# class AzureMediaStorage(AzureStorage):
#     account_name = os.environ.get('AZ_STORAGE_NAME', '') # Must be replaced by your <storage_account_name>
#     account_key = os.environ.get('AZ_STORAGE_KEY', '') # Must be replaced by your <storage_account_key>
#     azure_container = os.environ.get('AZ_MEDIA_CONTAINER', '')
#     expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = os.getenv('AZ_STORAGE_NAME', '') # Must be replaced by your <storage_account_name>
    account_key = os.getenv('AZ_STORAGE_KEY', '') # Must be replaced by your <storage_account_key>
    azure_container = os.getenv('AZ_STATIC_CONTAINER', '')
    expiration_secs = None