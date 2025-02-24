from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


class Item(models.Model):
    item_id=models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=50)
    store = models.CharField(max_length=50, choices=[("A", "Store A"), ("B", "Store B")])
    sale_price = models.IntegerField(null=True)
    cost_price = models.IntegerField(null=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=[("desert", "디저트류"), ("bread", "빵류"), ("cake", "케이크류")])
    best = models.BooleanField(default=False)
    new = models.BooleanField(default=False)
    show = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)
    item_name_eng = models.CharField(max_length=50, null=True)
    item_image = models.URLField(upload_to='', null=True, blank=True)  # 제품 사진


    def __str__(self):
        return f"Item {self.item_id}, {self.item_name}"


class NutritionInfo(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True, related_name='nutrition_info')  # 1:1 관계 (PK = FK)
    nutrition_weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1500)], null=True, blank=True)  # 중량(g)
    nutrition_calories = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5000)], null=True, blank=True)  # 칼로리(kcal)
    nutrition_sodium = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5000)], null=True, blank=True)  # 나트륨(mg)
    nutrition_sugar = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)  # 당류(g)
    nutrition_carbohydrates = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)  # 탄수화물(g)
    nutrition_saturated_fat = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)  # 포화지방(g)
    nutrition_trans_fat = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)  # 트랜스지방(g)
    nutrition_protein = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True)  # 단백질(g)

    def __str__(self):
        return f"Nutrition Info - {self.item.item_name}"


class Allergy(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, primary_key=True, related_name='allergy')  # 1:1 관계 (PK = FK)
    allergy_wheat = models.BooleanField(default=False)  # 밀 포함 여부
    allergy_milk = models.BooleanField(default=False)  # 우유 포함 여부
    allergy_egg = models.BooleanField(default=False)  # 계란 포함 여부
    allergy_soybean = models.BooleanField(default=False)  # 대두 포함 여부
    allergy_nuts = models.BooleanField(default=False)  # 견과류 포함 여부
    allergy_etc = models.CharField(max_length=100, null=True, blank=True)  # 기타 알레르기 정보

    def __str__(self):
        return f"Allergy Info - {self.item.item_name}"