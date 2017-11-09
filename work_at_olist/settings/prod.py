from os import environ
from .base import *


SECRET_KEY = environ['SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': environ['DB_HOST'],
        'NAME': environ['DB_NAME'],
        'USER': environ['DB_USER'],
        'PORT': environ['DB_PORT'],
        'PASSWORD': environ['DB_PASSWORD'],
    }
}
