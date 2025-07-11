import os
from .settings import *
from dotenv import load_dotenv
load_dotenv()


DEBUG = True

ALLOWED_HOSTS = ['localhost', '3.34.46.30', '127.0.0.1', 'www.devbreadscanso.shop', 'devbreadscanso.shop', "13.209.132.161"]

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

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',] # 인증 백엔드 설정

# S3 개발 환경 설정
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

# 미디어 파일을 S3에 저장하도록 설정
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# OpenAI API 키 추가
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ORM QUERY 로그 출력
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}

# CSRF 설정
CSRF_TRUSTED_ORIGINS = [
    "https://devbreadscanso.shop",
    "https://www.devbreadscanso.shop",
    "http://devbreadscanso.shop",
    "http://www.devbreadscanso.shop"
]