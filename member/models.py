from django.db import models

class Member(models.Model):
    member_id = models.CharField(max_length=12, primary_key=True)  # 회원 ID (PK)
    name = models.CharField(max_length=50)

