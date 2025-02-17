# EB(EC2) 운영환경
from .settings import *

# 운영환경에서는 반드시 False로 설정
DEBUG = True

ALLOWED_HOSTS = [
  'eb-breadscanso-env.eba-ivnsims9.ap-northeast-2.elasticbeanstalk.com',
  '52.79.158.104',
  'localhost',
]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'prod_db',  # 운영 DB 이름
#         'USER': 'prod_user',  # 운영 DB 계정
#         'PASSWORD': '운영 DB 비밀번호',
#         'HOST': '운영 DB EC2의 공인 IP',  # 정석이 만든 운영 DB의 IP
#         'PORT': '포트번호',
#     }
# }
