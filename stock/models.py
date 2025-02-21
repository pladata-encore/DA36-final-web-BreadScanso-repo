from django.db import models

class Ingredient(models.Model):
    ingredient_id=models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=50)
    store = models.CharField(max_length=50, choices=[("A", "Store A"), ("B", "Store B")])
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"Item {self.ingredient_id}, {self.ingredient_name}"