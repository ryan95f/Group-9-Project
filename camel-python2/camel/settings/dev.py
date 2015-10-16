from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'camel.db'),
    }
}

SECRET_KEY = 'a_secret_key'

INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
