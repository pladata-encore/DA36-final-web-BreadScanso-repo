from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models

class Member(models.Model):
    member_id = models.CharField(validators=[MinLengthValidator(4)], max_length=12, primary_key=True)  # 회원 ID (PK)
    member_type = models.CharField(max_length=20,
                                   choices=[("admin", "관리자"), ("owner", "대표"),
                                            ("manager", "점주"),("normal","일반회원")])
                                            # 회원 유형 (관리자, 점주, 대표, 일반 회원)
    name = models.CharField(validators=[MinLengthValidator(2)], max_length=50)
    sex = models.BooleanField()
    age_group = models.PositiveSmallIntegerField()  # 연령대 (20, 30, 40)
    phone_num = models.CharField(max_length=13,
                                 validators=[lambda value: ValidationError("13자리의 전화번호를 입력해주세요.")
                                 if len(value) != 13 else None])  # 전화번호
    member_password = models.CharField(validators=[MinLengthValidator(4)], max_length=12)  # 비밀번호
    email = models.EmailField()  # 이메일
    total_spent = models.IntegerField(default=0)  # 총 결제액
    points = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])  # 포인트
    last_visited = models.DateTimeField(null=True, blank=True)  # 마지막 방문일
    visit_count = models.IntegerField(default=0)  # 방문 횟수
    profile_image = models.ImageField(upload_to='', null=True, blank=True)  # 프로필 사진
    store_name = models.CharField(max_length=20)  # 매장 이름
    store_num = models.CharField(validators=[MinLengthValidator(10)], max_length=13)  # 매장 전화번호
    earning_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # 적립 비율

    def __str__(self):
        return f"Member {self.member_id}, {self.name}"