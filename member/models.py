from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from datetime import datetime
from django import forms
# from django.forms import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_id = models.CharField(validators=[MinLengthValidator(4)], max_length=12, primary_key=True)  # 회원 ID (PK)
    member_type = models.CharField(max_length=20,
                                   choices=[("admin", "관리자"), ("owner", "대표"),
                                            ("manager", "점주"), ("normal", "일반회원")])  # 회원 유형
    name = models.CharField(validators=[MinLengthValidator(2)], max_length=50)
    sex = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')], null=True, blank=True)  # 성별 (M/F)
    age_group = models.PositiveSmallIntegerField(
        null=True, blank=True,
        choices=[(10, "10대"), (20, "20대"), (30, "30대"), (40, "40대"), (50, "50대"), (60, "60대 이상")])  # 연령대 (20, 30, 40)
    phone_num = models.CharField(max_length=13)  # 전화번호
    member_password = models.CharField(validators=[MinLengthValidator(4)], max_length=20)  # 비밀번호
    email = models.EmailField()  # 이메일
    total_spent = models.IntegerField(default=0)  # 총 결제액
    points = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])  # 포인트
    last_visited = models.DateTimeField(null=True, blank=True)  # 마지막 방문일
    visit_count = models.IntegerField(default=0)  # 방문 횟수
    profile_image = models.ImageField(upload_to='', null=True, blank=True)  # 프로필 사진

    # 여기부터 매장 정보 ❗
    store = models.CharField(max_length=50, null=True, choices=[("A", "서초점"), ("B", "강남점")])
    store_num = models.CharField(max_length=13, null=True, blank=True, validators=[MinLengthValidator(10)])  # 매장 전화번호
    earning_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, default=0)  # 적립 비율
    store_address = models.TextField(null=True, blank=True)   # 매장 주소
    store_time = models.TextField(null=True, blank=True)   # 운영 시간
    store_notes = models.TextField(null=True, blank=True)  # 기타 사항

    def __str__(self):
        return f"회원 {self.member_id} - {self.name}"



class EventPost(models.Model):  # 이벤트 게시판 글 테이블
    event_id = models.AutoField(primary_key=True)  # 이벤트 게시글 아이디 (PK)
    member = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)  # 회원 아이디 (FK)
    title = models.CharField(max_length=30)  # 제목
    created_at = models.DateTimeField(auto_now_add=True)  # 등록일시
    updated_at = models.DateTimeField(auto_now=True)  # 수정일시
    content = models.ImageField(upload_to='', null=True, blank=True) # 이미지 내용
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
    author_id = models.CharField(max_length=50, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.qna:
            self.qna.is_answered = True
            self.qna.save()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"답변 - {self.qna.title}"

### Forms ###
class QuestionForm(forms.ModelForm):
    class Meta:
        model = QnA
        # fields = ['title', 'content', 'store']  # store 필드는 Model에서 자동으로 가져옴
        fields = ['title', 'content']
        labels = {
            'title': '제목',
            'content': '내용',
            # 'store': '매장선택'
        }

    # def __init__(self, *args, **kwargs):
    #     stores = kwargs.pop('stores', [])  # 🔥 추가: 전달된 stores 가져오기
    #     super().__init__(*args, **kwargs)
    #     self.fields['store'].choices = [("전체", "전체")] + [(store["id"], store["name"]) for store in stores]


# 회원정보수정
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # User 모델과 연결
    member_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=50)
    phone_num = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    age_group = models.CharField(max_length=10, choices=[("10대", "10대"), ("20대", "20대"), ("30대", "30대"), ("40대", "40대"),
                                                         ("50대", "50대"), ("60대 이상", "60대 이상")])
    sex = models.CharField(max_length=10, choices=[("남성", "남성"), ("여성", "여성")])
    profile_image = models.ImageField(upload_to="profile_images/", blank=True, null=True)

    def __str__(self):
        return self.name



# from django.db import models
# from django.core.exceptions import ValidationError
# from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
# from datetime import datetime
# from django.utils import timezone
#
#
# class Member(models.Model):
#     member_id = models.CharField(validators=[MinLengthValidator(4)], max_length=12, primary_key=True)  # 회원 ID (PK)
#     member_type = models.CharField(max_length=20,
#                                    choices=[("admin", "관리자"), ("owner", "대표"),
#                                             ("manager", "점주"), ("normal", "일반회원")])  # 회원 유형
#     name = models.CharField(validators=[MinLengthValidator(2)], max_length=50)
#     sex = models.CharField(max_length=1, choices=[('M', '남성'), ('F', '여성')])  # 성별 (M/F)
#     age_group = models.PositiveSmallIntegerField()  # 연령대 (20, 30, 40)
#     phone_num = models.CharField(max_length=13)  # 전화번호
#     member_password = models.CharField(validators=[MinLengthValidator(4)], max_length=20)  # 비밀번호
#     email = models.EmailField()  # 이메일
#     total_spent = models.IntegerField(default=0)  # 총 결제액
#     points = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])  # 포인트
#     last_visited = models.DateTimeField(null=True, blank=True)  # 마지막 방문일
#     visit_count = models.IntegerField(default=0)  # 방문 횟수
#     profile_image = models.ImageField(upload_to='', null=True, blank=True)  # 프로필 사진
#     store = models.CharField(max_length=50, null=True, choices=[("A", "Store A"), ("B", "Store B")])
#     store_num = models.CharField(max_length=13, null=True, blank=True, validators=[MinLengthValidator(10)])  # 매장 전화번호
#     earning_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, default=0)  # 적립 비율
#
#     def __str__(self):
#         return f"회원 {self.member_id} - {self.name}"
#
#
# class Notice(models.Model):  # 공지사항 글 테이블
#     notice_id = models.AutoField(primary_key=True)  # 공지사항 아이디 (PK)
#     title = models.CharField(max_length=30)  # 제목
#     member = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)  # 회원 아이디 (FK)
#     created_at = models.DateTimeField(auto_now_add=True)  # 등록일시
#     updated_at = models.DateTimeField(auto_now=True)  # 수정일시
#     content = models.TextField()  # 내용
#     view_count = models.IntegerField(default=0)  # 조회수
#     pinned = models.BooleanField(default=False)  # 상단 고정 여부
#     store = models.CharField(max_length=50, null=True, choices=[("A", "Store A"), ("B", "Store B")])  # 매장
#
#     def __str__(self):
#         return f"공지사항 {self.notice_id} - {self.title}"
#
#
# class EventPost(models.Model):  # 이벤트 게시판 글 테이블
#     event_id = models.AutoField(primary_key=True)  # 이벤트 게시글 아이디 (PK)
#     member = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)  # 회원 아이디 (FK)
#     title = models.CharField(max_length=30)  # 제목
#     created_at = models.DateTimeField(auto_now_add=True)  # 등록일시
#     updated_at = models.DateTimeField(auto_now=True)  # 수정일시
#     content = models.TextField()  # 내용
#     view_count = models.PositiveIntegerField(default=0)  # 조회수
#     is_pinned = models.BooleanField(default=False)  # 상단 고정 여부
#     store = models.CharField(max_length=50, null=True, choices=[("A", "Store A"), ("B", "Store B")])  # 매장
#
#     def __str__(self):
#         return f"이벤트 {self.event_id} - {self.title}"
#
#
# class QnA(models.Model):  # QnA 글 테이블
#     qna_id = models.AutoField(primary_key=True)  # QnA 아이디 (PK)
#     member = models.ForeignKey('Member', on_delete=models.SET_NULL, null=True)  # 회원 아이디 (FK)
#     title = models.CharField(max_length=30)  # 제목
#     created_at = models.DateTimeField(auto_now_add=True)  # 등록일시
#     updated_at = models.DateTimeField(auto_now=True)  # 수정일시
#     content = models.TextField()  # 내용
#     view_count = models.PositiveIntegerField(default=0)  # 조회수
#     is_answered = models.BooleanField(default=False)  # 답변 완료 여부
#     store = models.CharField(max_length=50, null=True, choices=[("A", "Store A"), ("B", "Store B")])  # 매장
#
#     def __str__(self):
#         return f"QnA {self.qna_id} - {self.title}"
#
#
# class QnAReply(models.Model):
#     qna = models.ForeignKey(QnA, on_delete=models.CASCADE, related_name="replies")  # 1:N 관계
#     content = models.TextField()  # 답변 내용
#     created_at = models.DateTimeField(auto_now_add=True)  # 등록일시, 처음 생성되면 변경 X
#     updated_at = models.DateTimeField(auto_now=True)  # 수정일시, 수정될 때마다 업데이트
#
#     def save(self, *args, **kwargs):
#         if self.qna:
#             self.qna.is_answered = True
#             self.qna.save()
#         super().save(*args, **kwargs)
#
#
#     def __str__(self):
#         return f"답변 - {self.qna.title}"
