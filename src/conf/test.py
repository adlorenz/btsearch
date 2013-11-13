from conf.default import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'USER': 'btsearch_app',
        'PASSWORD': '029ef8e6-1660-4a25-94b4-8d10f7d08adb',
        'HOST': 'localhost',
        'NAME': 'Btsearch2',
    }
}

EMAIL_SUBJECT_PREFIX = '[Btsearch][Test] '

LOGGING = create_logging_dict(location('../../logs/test'))

ALLOWED_HOSTS = ['test.btsearch.pl']
