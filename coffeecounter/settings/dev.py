from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__name__).resolve().parent

SECRET_KEY = '#cq@8ls2j9h)(^k0*nj$a!7c9-mwef958q9&&*x5krj!@jlt_e'
DEBUG=True

ALLOWED_HOSTS=[]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS =[
    os.path.join(BASE_DIR, 'static'),
]