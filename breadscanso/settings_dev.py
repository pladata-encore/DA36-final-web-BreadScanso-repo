import os
from .settings import *
from dotenv import load_dotenv
load_dotenv()


DEBUG = True

ALLOWED_HOSTS = ['localhost', '3.34.46.30']

# 개발 db
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_DEV_NAME'),
        'USER': os.getenv('DATABASE_DEV_USER'),
        'PASSWORD': os.getenv('DATABASE_DEV_PASSWORD'),
        'HOST': os.getenv('DATABASE_DEV_HOST'),
        'PORT': os.getenv('DATABASE_DEV_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}
