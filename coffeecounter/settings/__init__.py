from .base import *
import os
from dotenv import load_dotenv
load_dotenv()

# envVar=os.getenv('DATABASE_HOST')
# print(envVar)

# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
if os.getenv('ENVIRONMENT', None) == 'prod':
   from .production import *
else:
   from .dev import *