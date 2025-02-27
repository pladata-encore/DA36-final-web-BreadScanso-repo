from django.db import models
from member.models import Member
from menu.models import Item
from django.utils import timezone
from django.db import transaction
import random


# OrderInfo 주문정보
class OrderInfo(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_at = models.DateTimeField(auto_now_add=True)  # 주문 일시
    total_amount = models.IntegerField(default=0)  # 주문 총액
    store = models.CharField(max_length=50, choices=[("A", "Store A"), ("B", "Store B")])  # 매장
    earned_points = models.IntegerField(default=0)  # 적립 포인트
    used_points = models.IntegerField(default=0)  # 사용 포인트
    final_amount = models.IntegerField(default=0)  # 최종 결제 금액

    def calculate_earned_points(self):  # 적립 포인트 계산
        store_name = Member.objects.get(store=self.store)
        if store_name and store_name.earning_rate is not None:
            self.earned_points = int(self.total_amount * store_name.earning_rate)
        else:
            self.earned_points = 0
        return self.earned_points

    def calculate_final_amount(self, used_points=0):
        self.used_points = used_points
        self.final_amount = max(self.total_amount - used_points, 0)
        return self.final_amount

    def save(self, *args, **kwargs):
        if self._state.adding:  # 새로운 객체인 경우에만 계산
            self.calculate_earned_points()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id}"


# OrderItem 주문항목
class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)  # OrderInfo와 1:N 관계
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item_count = models.IntegerField()  # 제품 수량
    item_price = models.IntegerField(default=0)  # 제품 가격
    item_total = models.IntegerField(default=0)  # 제품 총액

    def save(self, *args, **kwargs):
        if self.item:
            self.item_price = self.item.sale_price   # 제품 가격 가져오기
            self.item.stock -= self.item_count    # 제품 재고 차감
            self.item.save()

        self.item_total = self.item_count * self.item_price  # 제품당 총액 계산
        super().save(*args, **kwargs)

        # 주문이 저장된 후, 해당 주문에 속한 모든 OrderItem을 기반으로 OrderInfo의 총액을 갱신함
        self.order.total_amount = sum(item.item_total for item in self.order.orderitem_set.all())
        self.order.save()

    def __str__(self):
        return f"Item {self.item} in Order {self.order.order_id}"


# PaymentInfo 결제정보
class PaymentInfo(models.Model):
    payment_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)  # OrderInfo와 1:N 관계
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)  # 회원 정보 추가
    payment_method = models.CharField(max_length=20, choices=[("credit", "카드"), ("cash", "현금")])  # 결제 방법
    payment_status = models.BooleanField(default=True)  # 결제 상태
    card_name = models.CharField(max_length=20, null=True, blank=True)  # 카드 이름
    pay_at = models.DateTimeField(default=timezone.now)
    approval_code = models.CharField(max_length=5, null=True, blank=True)  # 승인 번호
    used_points = models.IntegerField(default=0)  # 사용 포인트 필드 추가

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        if not is_new:
            try:
                previous_payment = PaymentInfo.objects.get(pk=self.pk)
                prev_status = previous_payment.payment_status
            except PaymentInfo.DoesNotExist:
                prev_status = None
        else:
            prev_status = None

        # 카드 결제 승인번호
        if self.payment_method == "credit" and not self.approval_code:
            self.approval_code = str(random.randint(10000, 99999))
        elif self.payment_method == "cash":
            self.approval_code = None

        with transaction.atomic():
            super().save(*args, **kwargs)

            if self.member:
                if is_new and self.payment_status:
                    # 회원 정보 업데이트
                    self.member.total_spent += self.order.total_amount
                    # 포인트 계산: 기존 포인트 + 적립 포인트 - 사용 포인트
                    self.member.points = self.member.points + self.order.earned_points - self.used_points
                    self.member.last_visited = self.order.order_at
                    self.member.visit_count += 1
                    self.member.save()

                # 결제 취소 시
                elif not is_new and prev_status is True and self.payment_status is False:
                    self.member.total_spent -= self.order.total_amount
                    # 포인트 계산: 기존 포인트 - 적립 포인트 + 사용 포인트
                    self.member.points = self.member.points - self.order.earned_points + self.used_points
                    self.member.save()

    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order.order_id}"