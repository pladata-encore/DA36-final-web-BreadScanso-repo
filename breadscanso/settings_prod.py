# EB(EC2) 운영환경
from .settings import *

# 운영환경에서는 반드시 False로 설정
DEBUG = True

ALLOWED_HOSTS = [
  'eb-breadscanso-env.eba-ivnsims9.ap-northeast-2.elasticbeanstalk.com',
  'breadscanso.shop','www.breadscanso.shop'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'PROD_NAME',
        'USER': 'PROD_USER',
        'PASSWORD': 'PROD_PASSWORD',
        'HOST': 'PROD_HOST',
        'PORT': 'PROD_PORT',
    }
}
