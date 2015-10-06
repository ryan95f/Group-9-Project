from .base import * # noqa

DEBUG = False

ALLOWED_HOSTS = []

SECRET_KEY = '8nol&9x!)@58k$ms1h_f0_ir^krld$q!az4b4+_#@0=-(_850c'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'camel',
        'USER': 'humpty',
        'PASSWORD': '12345',
        'HOST': 'localhost',
        'PORT': '',
    }
}

ALLOWED_HOSTS = ['camel.maths.cf.ac.uk']
