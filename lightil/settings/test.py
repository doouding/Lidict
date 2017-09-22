"""
This setting file is created for CI
"""
from .base import *

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'NAME': 'lightil',
        'USER': 'root',
        'PASSWORD': ''
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8$zd&J52iqt;w>pDE.UYS)osUM0A,W{jpBMU71mLz3Q4$!{Xn?'

# Some django app haven't complete
# thus add it to INSTALLED_APPS may cause
# ci build fail

# Remove it once all django app is done

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'jwt_auth.apps.JwtAuthConfig',
    'rest_framework'
]
