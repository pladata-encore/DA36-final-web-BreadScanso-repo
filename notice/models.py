from django.db import models

# Create your models here.

class Notice(models.Model):
    title = models.CharField(max_length=255)  # 공지 제목
    content = models.TextField()  # 공지 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 날짜
    updated_at = models.DateTimeField(auto_now=True)  # 수정 날짜
