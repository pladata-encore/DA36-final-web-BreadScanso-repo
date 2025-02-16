from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from datetime import datetime
from django.utils import timezone


class Member(models.Model):
    member_id = models.CharField(validators=[MinLengthValidator(4)], max_length=12, primary_key=True)  # 회원 ID (PK)
    member_type = models.CharField(max_length=20,
                                   choices=[("admin", "관리자"), ("owner", "대표"),
                                            ("manager", "점주"), ("normal", "일반회원")])  # 회원 유형
    name = models.CharField(validators=[MinLengthValidator(2)], max_length=50)
    sex = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')])  # 성별 (M/F)
    age_group = models.PositiveSmallIntegerField()  # 연령대 (20, 30, 40)
    phone_num = models.CharField(max_length=13)  # 전화번호
    member_password = models.CharField(validators=[MinLengthValidator(4)], max_length=20)  # 비밀번호
    email = models.EmailField()  # 이메일
    total_spent = models.IntegerField(default=0)  # 총 결제액
    points = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])  # 포인트
    last_visited = models.DateTimeField(null=True, blank=True)  # 마지막 방문일
    visit_count = models.IntegerField(default=0)  # 방문 횟수
    profile_image = models.ImageField(upload_to='', null=True, blank=True)  # 프로필 사진
    store = models.CharField(max_length=50, null=True, choices=[("A", "Store A"), ("B", "Store B")])
    store_num = models.CharField(max_length=13, null=True, blank=True, validators=[MinLengthValidator(10)])  # 매장 전화번호
    earning_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, default=0)  # 적립 비율

    def __str__(self):
        return f"회원 {self.member_id} - {self.name}"


class Notice(models.Model):  # 공지사항 글 테이블
    notice_id = models.AutoField(primary_key=True)  # 공지사항 아이디 (PK)
    title = models.CharField(max_length=30)  # 제목
    member = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)  # 회원 아이디 (FK)
    created_at = models.DateTimeField(auto_now_add=True)  # 등록일시
    updated_at = models.DateTimeField(auto_now=True)  # 수정일시
    content = models.TextField()  # 내용
    view_count = models.IntegerField(default=0)  # 조회수
    pinned = models.BooleanField(default=False)  # 상단 고정 여부
    store = models.CharField(max_length=50, null=True, choices=[("A", "Store A"), ("B", "Store B")])  # 매장

    def __str__(self):
        return f"공지사항 {self.notice_id} - {self.title}"


class EventPost(models.Model):  # 이벤트 게시판 글 테이블
    event_id = models.AutoField(primary_key=True)  # 이벤트 게시글 아이디 (PK)
    member = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)  # 회원 아이디 (FK)
    title = models.CharField(max_length=30)  # 제목
    created_at = models.DateTimeField(auto_now_add=True)  # 등록일시
    updated_at = models.DateTimeField(auto_now=True)  # 수정일시
    content = models.TextField()  # 내용
    view_count = models.PositiveIntegerField(default=0)  # 조회수
    is_pinned = models.BooleanField(default=False)  # 상단 고정 여부
    store = models.CharField(max_length=50, null=True, choices=[("A", "Store A"), ("B", "Store B")])  # 매장

    def __str__(self):
        return f"이벤트 {self.event_id} - {self.title}"


class QnA(models.Model):  # QnA 글 테이블
    qna_id = models.AutoField(primary_key=True)  # QnA 아이디 (PK)
    member = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)  # 회원 아이디 (FK)
    title = models.CharField(max_length=30)  # 제목
    created_at = models.DateTimeField(auto_now_add=True)  # 등록일시
    updated_at = models.DateTimeField(auto_now=True)  # 수정일시
    content = models.TextField()  # 내용
    view_count = models.PositiveIntegerField(default=0)  # 조회수
    is_answered = models.BooleanField(default=False)  # 답변 완료 여부
    store = models.CharField(max_length=50, null=True, choices=[("A", "Store A"), ("B", "Store B")])  # 매장

    def __str__(self):
        return f"QnA {self.qna_id} - {self.title}"


class QnAReply(models.Model):
    qna = models.ForeignKey(QnA, on_delete=models.CASCADE, related_name="replies")  # 1:N 관계
    content = models.TextField()  # 답변 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 등록일시, 처음 생성되면 변경 X
    updated_at = models.DateTimeField(auto_now=True)  # 수정일시, 수정될 때마다 업데이트

    def __str__(self):
        return f"답변 - {self.qna.title}"
