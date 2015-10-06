from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'data') + 'camel-test.db',
    }
}

SECRET_KEY = 'a_secret_key'