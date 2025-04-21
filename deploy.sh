#!/bin/bash

# 1. 작업 디렉토리로 이동
cd ~/breadscanso-dev

# 2. 도커 이미지 최신 버전 가져오기
echo "[1/5] Pulling latest image..."
docker pull ${DOCKER_DEV_IMAGE}

# 3. 기존 컨테이너 중지 및 삭제
echo "[2/5] Stopping and removing old container..."
docker stop dev-backend-container 2>/dev/null || true
docker rm dev-backend-container 2>/dev/null || true

# 4. 새 컨테이너 실행
echo "[3/5] Starting new container..."
docker run -d \
  --name dev-backend-container \
  -p 8000:8000 \
  --env-file /home/ubuntu/.env \
  -e DJANGO_SETTINGS_MODULE=breadscanso.settings_dev \
  ${DOCKER_DEV_IMAGE}

# 5. 확인 메시지 출력
echo "[4/5] Deployment complete!"
docker ps | grep dev-backend-container

echo "[5/5] DONE"
