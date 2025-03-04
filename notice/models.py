from django.db import models
from member.models import Member
from django.contrib.auth.models import User

# Create your models here.
class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    member = models.ForeignKey('member.Member', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    view_count = models.IntegerField(default=0)
    pinned = models.BooleanField(default=False)
    store = models.CharField(max_length=50, null=True, choices=[("A", "서초점"), ("B", "강남점")])
    notice_image = models.ImageField(upload_to='', null=True, blank=True)  # 제품 사진

    def __str__(self):
        return f"공지사항 {self.notice_id} - {self.title}"
