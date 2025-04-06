# 개발 환경용 gunicorn 설정

# workers 최소화 (개발 환경이므로)
workers = 1

# bind 주소/포트
bind = '0.0.0.0:8000'

# worker_class 설정
worker_class = 'uvicorn.workers.UvicornWorker'

# wsgi_app 실행한 모듈 application
wsgi_app = 'breadscanso.asgi:application'