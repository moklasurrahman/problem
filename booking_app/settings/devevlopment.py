from .base import *

from pathlib import Path
from .utils import get_secret

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEBUG = True
DEBUG_TOOLBAR = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", 'uralholidays.com', "uraltravelandtours.com", "uralholidays.com"]
CORS_ALLOWED_ORIGINS = []
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

SECRET_KEY = 'django-insecure-+mqi^t_drfkpft1phfe1pwwr9u5#phb11u9^o4u!nsra)s#6l!'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': get_secret('DB_NAME'),
#         'USER': get_secret('DB_USER'),
#         'PASSWORD': get_secret('DB_PASSWORD'),
#         'HOST': get_secret('DB_HOST'),
#         'PORT': get_secret('DB_PORT'),
#     },
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
#     'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'uralholiday',
#        'USER': 'chris',
#        'PASSWORD': '',
#        'HOST': 'localhost',
#        'PORT': '',
#    }
}

LANGUAGE_CODE = 'en-us'

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = get_secret('SENDGRID_API_KEY')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
DEFAULT_FROM_EMAIL = 'Uralholidays Team <admin@uralholidays.com>'

STATIC_ROOT = BASE_DIR / "static/assets"
MEDIA_ROOT = BASE_DIR / "static/media"

STATIC_URL = '/static/'
MEDIA_URL = 'https://static.rhizo.us/media/'

if DEBUG and DEBUG_TOOLBAR:
    INSTALLED_APPS += (
        'debug_toolbar',
        'django_extensions',
        #'profiler'
    )

    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware',]
    #MIDDLEWARE_CLASSES += ('profiler.middleware.ProfilerMiddleware',)
    #DEBUG_TOOLBAR_CONFIG = {
    #    'INTERCEPT_REDIRECTS': False,
    #}

    INTERNAL_IPS = (
        '127.0.0.1',
    )

if DEBUG:
    # Using mailcatcher
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_USER = 'mdtajuddin8089@gmail.com'
    EMAIL_HOST_PASSWORD = 'oscw bfwf wqmr zoka'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = False