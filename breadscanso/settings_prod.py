# EB(EC2) 운영환경
from .settings import *
import os

# 운영환경에서는 반드시 False로 설정
DEBUG = False

ALLOWED_HOSTS = [
  'eb-breadscanso2-env.eba-ivnsims9.ap-northeast-2.elasticbeanstalk.com', # eb 도메인
  '172.31.33.23', # ec2 private ip
  'breadscanso.shop',
  'www.breadscanso.shop',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_PROD_NAME'),
        'USER': os.getenv('DATABASE_PROD_USER'),
        'PASSWORD': os.getenv('DATABASE_PROD_PASSWORD'),
        'HOST': os.getenv('DATABASE_PROD_HOST'),
        'PORT': os.getenv('DATABASE_PROD_PORT'),
    }
}

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend',] # 인증 백엔드 설정

# CSRF(Cross-Site Request Forgery) 보호 정책
CSRF_TRUSTED_ORIGINS = [
    "https://www.breadscanso.shop",
    "https://breadscanso.shop"
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


# S3 운영 환경 설정
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
AWS_S3_CUSTOM_DOMAIN = f"https://{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com"

# 미디어 파일을 S3에 저장하도록 설정
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"















# # EB(EC2) 운영환경
# from .settings import *
# import os
#
# # 운영환경에서는 반드시 False로 설정
# DEBUG = True
#
# ALLOWED_HOSTS = [
#   'eb-breadscanso2-env.eba-ivnsims9.ap-northeast-2.elasticbeanstalk.com', # eb 도메인
#   '172.31.33.23', # ec2 private ip
#   'breadscanso.shop',
#   'www.breadscanso.shop',
# ]
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': os.getenv('DATABASE_PROD_NAME'),
#         'USER': os.getenv('DATABASE_PROD_USER'),
#         'PASSWORD': os.getenv('DATABASE_PROD_PASSWORD'),
#         'HOST': os.getenv('DATABASE_PROD_HOST'),
#         'PORT': os.getenv('DATABASE_PROD_PORT'),
#     }
# }
