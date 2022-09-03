import os
from dotenv import load_dotenv

from neolibrary.settings import *

load_dotenv()

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DATABASE_NAME"),
        'USER': os.getenv("DATABASE_USER"),
        'HOST': os.getenv("DATABASE_HOST"),
        'PORT': '5432',
    },
}

# ALLOWED_HOSTS = ["*"]

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

DEBUG = True
SECRET_KEY = os.getenv("SECRET_KEY")
