import boto3
from botocore.exceptions import NoCredentialsError
import os
from uuid import uuid4
from django.conf import settings
import zipfile
import tempfile
import mimetypes

def upload_product_image_to_s3(file, folder="product_images"):
    """제품 이미지를 S3에 업로드하고 URL을 반환하는 함수"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    file_extension = file.name.split(".")[-1]
    unique_filename = f"{folder}/{uuid4().hex}.{file_extension}"

    try:
        s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, unique_filename)
        return f"{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_filename}"
    except NoCredentialsError:
        raise Exception("AWS 자격증명을 찾을 수 없습니다.")
    except Exception as e:
        raise Exception(f"S3 업로드 실패: {str(e)}")

def upload_multiple_images_to_s3(files, item_id, folder="product_images"):
    """여러 장의 이미지를 S3에 업로드하고 URL 목록을 반환하는 함수"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    
    uploaded_urls = []
    
    for file in files:
        file_extension = file.name.split(".")[-1]
        unique_filename = f"{folder}/{item_id}/{uuid4().hex}.{file_extension}"
        
        try:
            s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, unique_filename)
            url = f"{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_filename}"
            uploaded_urls.append(url)
        except Exception as e:
            raise Exception(f"이미지 업로드 실패: {str(e)}")
    
    return uploaded_urls

def upload_zip_to_s3(zip_file, item_id, folder="product_images"):
    """ZIP 파일의 내용을 추출하여 이미지와 동영상만 S3에 업로드"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    
    uploaded_urls = []
    allowed_mime_types = ['image/', 'video/']
    valid_files_found = False  # 유효한 파일이 하나라도 있는지 확인하는 플래그
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # ZIP 파일 압축 해제
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # 압축해제된 모든 파일 순회
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                # 파일 형식 확인 (이미지 또는 동영상만 허용)
                mime_type, _ = mimetypes.guess_type(file_path)
                if mime_type and any(mime_type.startswith(allowed_type) for allowed_type in allowed_mime_types):
                    valid_files_found = True  # 유효한 파일이 하나라도 있음
                    file_extension = file.split(".")[-1].lower()
                    unique_filename = f"{folder}/{item_id}/zip_{uuid4().hex}.{file_extension}"
                    
                    try:
                        with open(file_path, 'rb') as f:
                            s3.upload_fileobj(f, settings.AWS_STORAGE_BUCKET_NAME, unique_filename)
                            url = f"{settings.AWS_S3_CUSTOM_DOMAIN}/{unique_filename}"
                            uploaded_urls.append(url)
                    except Exception as e:
                        raise Exception(f"ZIP 파일 내 항목 업로드 실패: {str(e)}")
    
    # 유효한 파일이 하나도 없는 경우 예외 발생
    if not valid_files_found:
        raise Exception("ZIP 파일 내에 이미지나 동영상 파일이 없습니다.")
    
    return uploaded_urls