# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-21 12:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_auto_20180117_2207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='original_food',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meal_food', to='food.Food', verbose_name='Alimento'),
        ),
    ]
