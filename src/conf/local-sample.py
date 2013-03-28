"""
Sample settings file for local environment

Populate this file with correct settings and save as local.py
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'mysql-username',
        'PASSWORD': 'mysql-password',
        'HOST': 'localhost',
        'NAME': 'Btsearch2',
    }
}