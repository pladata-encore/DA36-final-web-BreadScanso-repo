# Generated by Django 5.1.6 on 2025-03-05 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0003_notice_notice_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='notice_image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
