from django.db import models
from member.models import Member
# Create your models here.
class Notice(models.Model):  # 공지사항 글 테이블
    notice_id = models.AutoField(primary_key=True)  # 공지사항 아이디 (PK)
    title = models.CharField(max_length=30)  # 제목
    member = models.ForeignKey('member.Member', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 등록일시
    updated_at = models.DateTimeField(auto_now=True)  # 수정일시
    content = models.TextField()  # 내용
    view_count = models.IntegerField(default=0)  # 조회수
    pinned = models.BooleanField(default=False)  # 상단 고정 여부
    store = models.CharField(max_length=50, null=True, choices=[("A", "Store A"), ("B", "Store B")])  # 매장

    def __str__(self):
        return f"공지사항 {self.notice_id} - {self.title}"