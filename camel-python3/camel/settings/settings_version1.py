# django settings for camel project.

import os
SITE_ROOT = os.path.dirname(os.path.dirname(__file__))
TEX_ROOT  = os.path.join(SITE_ROOT, 'data/tex/')
PDF_ROOT  = os.path.join(SITE_ROOT, 'data/pdf/')
CSV_ROOT  = os.path.join(SITE_ROOT, 'data/csv/')
XML_ROOT  = os.path.join(SITE_ROOT, 'data/xml/')

import socket
if socket.gethostname().startswith('morlais'):
    LIVEHOST = True
else:
    LIVEHOST = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zm8*_50*9-sziwme0*@n*^zb=g&(r^wwft5#q+me-345z=377*'

# basic settings for development/production server
if LIVEHOST:
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    ALLOWED_HOSTS = ['camel.maths.cf.ac.uk']
else:
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    ALLOWED_HOSTS = []

# basic settings for development/production server
if LIVEHOST:
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
else:
    DATABASES = {
	    'default': {
    	    'ENGINE': 'django.db.backends.sqlite3',
    	    'NAME': os.path.join(SITE_ROOT, 'data') + '/camel.db',
	    }
    }

# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    # 'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'mptt',
	'camel',
    'review',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'camel.urls'
WSGI_APPLICATION = 'camel.wsgi.application'

# location
TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
LANGUAGES = (
    ('en', 'English'),
    ('cy', 'Cymraeg'),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True

# media (user uploaded)
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')
MEDIA_URL = '/media/'

# static files (css, js, png)
STATIC_ROOT = os.path.join(SITE_ROOT, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
	os.path.join(SITE_ROOT, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# templates
TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# redirect
LOGIN_URL = '/login/'

# logging config
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
	},
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
	    'mail_admins': {
	        'level': 'ERROR',
	        'filters': ['require_debug_false'],
	        'class': 'django.utils.log.AdminEmailHandler'
	    },
		'file': {
			'level': 'INFO',
			'class': 'logging.FileHandler',
			'filename': 'camel.log',
			'formatter': 'verbose'
	    },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }

    },
    'loggers': {
	     'django.request': {
	         'handlers': ['mail_admins'],
	         'level': 'ERROR',
	         'propagate': True,
	     },
	    'camel': {
	        'handlers': ['file'],
	        'level': 'DEBUG',
	    },
	    'django': {
	        'handlers': ['null'],
	        'level': 'INFO',
	        'propagate': True,
	    }
    }
}
