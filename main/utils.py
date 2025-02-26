import boto3
from botocore.exceptions import NoCredentialsError
import os
from uuid import uuid4

from django.conf import settings


def upload_profile_image_to_s3(file, folder="profile_images"):
    """S3에 파일을 업로드하고 URL을 반환하는 함수"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    file_extension = file.name.split(".")[-1]  # 확장자 추출
    unique_filename = f"{folder}/{uuid4().hex}.{file_extension}"  # UUID로 파일명 설정

    # s3client.upload_file(업로드할 파일명, 버킷명, 저장할 경로)
    # 수업에서는 upload_file을 썼지만, 웹앱에서 업로드 되면 보통 객체로 전달되기 때문에 upload_fileobj이 더 적절해 보여서 사용했습니다.
    s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, unique_filename)

    return f"{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_filename}"