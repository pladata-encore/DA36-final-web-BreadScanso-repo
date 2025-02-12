from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    precondition = models.CharField(max_length=15, blank=False, null=False)  # 필수 입력
    profile_image = models.ImageField(upload_to='profile_pics', blank=True, null=True) # 프로필 이미지 업로드
