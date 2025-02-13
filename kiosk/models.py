from django.db import models
from member.models import Member


class OrderInfo(models.Model):
    order_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, to_field='member_id')
    order_datetime = models.DateTimeField()
    total_price = models.IntegerField()
    earned_points = models.IntegerField()
    store = models.CharField(max_length=50, choices=[("A", "Store A"), ("B", "Store B")])  # Enum 타입 대체

    def __str__(self):
        return f"Order {self.order_id}"

class OrderProduct(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)  # FK 연결
    item_id = models.IntegerField()
    count = models.IntegerField()
    item_price = models.IntegerField()
    item_total = models.IntegerField()

    def __str__(self):
        return f"Item {self.item_id} in Order {self.order.order_id}"

class PaymentInfo(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)  # FK 연결
    payment_method = models.CharField(max_length=20, choices=[("credit", "Credit Card"), ("cash", "Cash")])  # Enum 대체
    payment_status = models.BooleanField(default=False)
    card_name = models.CharField(max_length=10, null=True, blank=True)
    approval_code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order.order_id}"
