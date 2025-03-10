import boto3
from botocore.exceptions import NoCredentialsError
import os
from uuid import uuid4
from django.conf import settings

# def upload_notice_image_to_s3(file, folder="notice_images"):
#     """공지사항 이미지를 S3에 업로드하고 URL을 반환하는 함수"""
#     s3 = boto3.client(
#         "s3",
#         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#         region_name=settings.AWS_S3_REGION_NAME,
#     )
#
#     file_extension = file.name.split(".")[-1]
#     unique_filename = f"{folder}/{uuid4().hex}.{file_extension}"
#
#     try:
#         s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, unique_filename)
#         return f"{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_filename}"
#     except NoCredentialsError:
#         raise Exception("AWS 자격증명을 찾을 수 없습니다.")
#     except Exception as e:
#         raise Exception(f"S3 업로드 실패: {str(e)}")

# ------------------------------------
# 로컬 업로드 용
def upload_notice_image_to_s3(file, folder="notice_images"):
    file_extension = file.name.split(".")[-1]
    unique_filename = f"{folder}/{uuid4().hex}.{file_extension}"
    file_path = os.path.join(settings.MEDIA_ROOT, unique_filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return f"{settings.MEDIA_URL}{unique_filename}"