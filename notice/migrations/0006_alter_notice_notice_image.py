# Generated by Django 5.1.6 on 2025-03-11 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0005_alter_notice_notice_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='notice_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
