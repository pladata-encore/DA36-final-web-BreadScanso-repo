from django.db import models
from member.models import Member



class OrderInfo(models.Model):
    order_id = models.AutoField(primary_key=True)  # 자동 증가 PK
    # member = models.ForeignKey('member.Member', on_delete=models.CASCADE, to_field='member_id', null=True, blank=True)
    order_datetime = models.DateTimeField(auto_now_add=True)  # 주문 시간 (자동 추가)
    total_price = models.IntegerField()  # 총 가격
    earned_points = models.IntegerField()  # 적립 포인트
    store = models.CharField(max_length=50, choices=[("A", "Store A"), ("B", "Store B")])  # 매장 선택

    def __str__(self):
        return f"Order {self.order_id}"
