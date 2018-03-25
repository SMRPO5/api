from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'smrpo',
        'USER': 'smrpo',
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}

MEDIA_ROOT = '/app/media'
STATIC_ROOT = '/app/static'

STATIC_URL = '/api/static/'
MEDIA_URL = '/api/media/'
