# Generated by Django 5.1.1 on 2024-09-25 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ashaapp1', '0003_skincarecheck'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='mobile',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
