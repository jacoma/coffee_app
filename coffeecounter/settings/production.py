from coffeecounter.settings import *
import os

SECRET_KEY = os.getenv('SECRET_KEY')


DEBUG = True

# Configure the domain name using the environment variable
# that Azure automatically creates for us.
ALLOWED_HOSTS = [os.getenv('WEBSITE_HOSTNAME'), '127.0.0.1']

# WhiteNoise configuration
MIDDLEWARE = [                                                                   
    'django.middleware.security.SecurityMiddleware',
# Add whitenoise middleware after the security middleware                             
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',                      
    'django.middleware.common.CommonMiddleware',                                 
    'django.middleware.csrf.CsrfViewMiddleware',                                 
    'django.contrib.auth.middleware.AuthenticationMiddleware',                   
    'django.contrib.messages.middleware.MessageMiddleware',                      
    'django.middleware.clickjacking.XFrameOptionsMiddleware',                    
]
 
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'storages.backends.azure_storage.AzureStorage'
# AZURE_ACCOUNT_NAME = os.getenv('AZ_STORAGE_ACCOUNT_NAME')
# AZURE_CONTAINER = os.getenv('AZ_STORAGE_CONTAINER')
# AZURE_ACCOUNT_KEY = os.getenv('AZ_STORAGE_KEY')

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
STATICFILES_STORAGE = 'storages.backends.custom_azure.AzureStaticStorage'
STATIC_LOCATION = os.getenv("AZ_STATIC_CONTAINER")
# MEDIA_LOCATION = "media"

AZURE_ACCOUNT_NAME = os.getenv('AZ_STORAGE_NAME')
AZURE_CUSTOM_DOMAIN = f'{AZURE_ACCOUNT_NAME}.blob.core.windows.net'
STATIC_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
# MEDIA_URL = f'https://{AZURE_CUSTOM_DOMAIN}/{MEDIA_LOCATION}/'

DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.postgresql', # removed _psycopg2
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASS'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}



