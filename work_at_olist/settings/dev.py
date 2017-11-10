from .base import *


DEBUG = True

SECRET_KEY = 'jwztgcq*!q55q^l8hfd5%rc0bz+!llp+c#u!z2hry_-m+mt5sv'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PORT': 5432,
        'PASSWORD': '',
    }
}
