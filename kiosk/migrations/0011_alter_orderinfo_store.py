# Generated by Django 5.1.6 on 2025-03-11 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosk', '0010_merge_20250303_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='store',
            field=models.CharField(choices=[('A', '서초점'), ('B', '강남점')], max_length=50),
        ),
    ]
