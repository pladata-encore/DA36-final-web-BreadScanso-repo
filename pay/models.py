from django.db import models

class Purchase(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100)
    price = models.IntegerField()
