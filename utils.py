import boto3
import os
from uuid import uuid4

def upload_to_s3(file, folder="profile_images"):
    """S3에 파일을 업로드하고 URL을 반환하는 함수"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_S3_REGION_NAME"),
    )

    file_extension = file.name.split(".")[-1]  # 확장자 추출
    unique_filename = f"{folder}/{uuid4().hex}.{file_extension}"  # UUID로 파일명 설정

    s3.upload_fileobj(file, os.getenv("AWS_STORAGE_BUCKET_NAME"), unique_filename)

    return f"{os.getenv('AWS_S3_CUSTOM_DOMAIN')}/{unique_filename}"

def upload_product_image_to_s3(file, folder="product_images"):
    """제품 이미지를 S3에 업로드하고 URL을 반환하는 함수"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_S3_REGION_NAME"),
    )

    file_extension = file.name.split(".")[-1]  # 확장자 추출
    unique_filename = f"{folder}/{uuid4().hex}.{file_extension}"  # UUID로 파일명 설정

    s3.upload_fileobj(file, os.getenv("AWS_STORAGE_BUCKET_NAME"), unique_filename)

    return f"{os.getenv('AWS_S3_CUSTOM_DOMAIN')}/{unique_filename}"