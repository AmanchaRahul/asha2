# Generated by Django 3.2.1 on 2024-10-15 07:24

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ashaapp1', '0015_auto_20241014_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diabeteschallengeimage',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255, verbose_name='image'),
        ),
    ]