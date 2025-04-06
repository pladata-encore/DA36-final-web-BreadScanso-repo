#!/bin/bash

cd ~/breadscanso-dev

cat > docker-compose.yml << EOF
version: '3'
services:
  web:
    image: ${DOCKER_IMAGE}
    restart: always
    environment:
      - DJANGO_SETTINGS_MODULE=breadscanso.settings_dev
    ports:
      - "80:8000"
    volumes:
      - ./static:/app/static
      - ./media:/app/media
    env_file:
      - .env
EOF

docker pull ${DOCKER_DEV_IMAGE}
docker-compose down
docker-compose up -d
