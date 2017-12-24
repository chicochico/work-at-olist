SECRET_KEY = 'jwztgcq*!q55q^l8hfd5%rc0bz+!llp+c#u!z2hry_-m+mt5sv'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
