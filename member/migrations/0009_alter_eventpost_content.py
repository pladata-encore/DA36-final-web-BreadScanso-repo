# Generated by Django 5.1.6 on 2025-02-28 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_member_store_address_member_store_notes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpost',
            name='content',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
