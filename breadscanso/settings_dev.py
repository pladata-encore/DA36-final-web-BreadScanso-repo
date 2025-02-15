import os

DEBUG = True

ALLOWED_HOSTS = ['localhost', '3.34.46.30']

# 개발 db
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # MySQL 엔진 사용
        'NAME': os.getenv('DATABASE_NAME'),                      # 데이터베이스 이름 (MySQL에서 만든 DB)
        'USER': os.getenv('DATABASE_USER'),                     # MySQL 사용자
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),              # MySQL 비밀번호
        'HOST': os.getenv('DATABASE_HOST'),                 # 서버의 공인 IP 또는 도메인
        'PORT': os.getenv('DATABASE_PORT'),                          # MySQL 기본 포트
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"  # 엄격한 SQL 모드 설정
        }
    }
}
