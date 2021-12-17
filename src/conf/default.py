# -*- coding: utf-8 -*-

import os

location = lambda *path: os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', *path)

# Default to production settings
DEBUG = False

ADMINS = (
    ('Alerts', 'd.lorenz@btsearch.pl'),
)

MANAGERS = ADMINS

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'django_extensions',

    'btsearch.bts',
    'btsearch.uke',
    'btsearch.map',
    'btsearch.panel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'btsearch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'btsearch.context_processors.metadata',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'pl'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_COOKIE_HTTPONLY = True  # Default value

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)  # Default Value

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'

SITE_ID = 1

# Additional locations of static files
STATICFILES_DIRS = (
    location('static/'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# # URL prefix for admin static files -- CSS, JavaScript and images.
# # Make sure to use a trailing slash.
# # Examples: "http://foo.com/static/admin/", "/static/admin/".
# ADMIN_MEDIA_PREFIX = '/static/admin/'

# TEMPLATE_DIRS = (
#     location('templates'),
# )


def create_logging_dict(root):
    """
    Create a logging dict using the passed root for log files
    """
    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'filters': ['require_debug_true'],
                'formatter': 'verbose'
            },
            'error_file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(root, 'errors.log'),
                'maxBytes': 1024*1024*100,
                'backupCount': 3,
                'formatter': 'verbose'
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': False,
            },
            'django.request': {
                'handlers': ['error_file', 'mail_admins'],
                'level': 'ERROR',
                'propagate': False,
            },
            # Enable this logger to see SQL queries
            'django.db.backends': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        }
    }

# This setting should be overridden in each environment
LOGGING = create_logging_dict(location('logs'))

INTERNAL_IPS = ('127.0.0.1',)

MAP_ICON_PATH = STATIC_URL + 'map_icons/'
