from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'smrpo',
        'USER': 'smrpo',
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': '5432',
    }
}

MEDIA_ROOT = '/app/media'
STATIC_ROOT = '/app/static'

DEFENDER_REDIS_URL = os.environ.get('REDIS_HOST', 'redis://redis:6379/0')

STATIC_URL = '/api/static/'
MEDIA_URL = '/api/media/'
