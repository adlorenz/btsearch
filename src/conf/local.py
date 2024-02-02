import os
from .default import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': os.environ.get('MYSQL_USER'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD'),
        'HOST': os.environ.get('MYSQL_HOST'),
        'NAME': os.environ.get('MYSQL_DATABASE'),
        'charset': 'utf8mb4', 
        'SECRET_KEY': 'klucz'
    }
}
