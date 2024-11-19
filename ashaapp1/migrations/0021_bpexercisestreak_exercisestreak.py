# Generated by Django 3.2.1 on 2024-11-16 06:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ashaapp1', '0020_delete_exercisestreak'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExerciseStreak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_activity_date', models.DateField()),
                ('current_streak', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user',)},
            },
        ),
        migrations.CreateModel(
            name='BPExerciseStreak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_activity_date', models.DateField()),
                ('current_streak', models.IntegerField(default=0)),
                ('weekly_exercises', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user',)},
            },
        ),
    ]