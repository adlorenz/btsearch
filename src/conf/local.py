from .default import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'user',
        'PASSWORD': 'pass',
        'HOST': 'mysql.local',
        'NAME': 'btsearch',
        'charset': 'utf8mb4', 
        'SECRET_KEY': 'klucz'
    }
}
