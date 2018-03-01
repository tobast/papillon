""" Local settings """

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@-=k62(!6%kj7f$%i*n)u=7e(+ncjx^&ia=_ah@0v+dur1q4k^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Time zone
TIME_ZONE = 'UTC'

# Static files' directory
STATIC_ROOT = os.path.join(PUBLIC_DIR, 'static')

# Media directory
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Sub-directroy of MEDIA_DIR in which the upload will be saved
UPLOAD_DIR = os.path.join('private', 'uploads')
