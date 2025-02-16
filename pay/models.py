# from django.db import models
# from django.shortcuts import render, get_object_or_404
#
# class Purchase(models.Model):
#     date = models.DateTimeField()
#     store_name = models.CharField(max_length=255)
#     product_name = models.CharField(max_length=255)
#     quantity = models.IntegerField()
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)
#     total_quantity = models.IntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)  # 총 가격
#     reward_points = models.IntegerField()  # 적립 포인트
#     payment_method = models.CharField(
#         max_length=20,
#         choices=[("card", "카드"), ("simple", "간편결제")],
#     )
#     member_status = models.CharField(
#         max_length=10,
#         choices=[("member", "회원"), ("non-member", "비회원")],
#     )
#     is_cancelled = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"{self.date} - {self.store_name} - {self.product_name}"
#
#
# class PurchaseDetail(models.Model):
#     purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="details")
#     product_name = models.CharField(max_length=255)
#     quantity = models.IntegerField()
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#
#     def __str__(self):
#         return f"{self.purchase.date} - {self.product_name}"
#
#
# class PayCancel(models.Model):
#     purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name="cancel_info")
#     cancel_date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"취소됨: {self.purchase.date} - {self.purchase.product_name}"