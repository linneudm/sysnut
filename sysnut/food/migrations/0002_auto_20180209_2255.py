# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-02-10 01:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patient', '0001_initial'),
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='substituteitem',
            name='food_analysis_substitute',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substitute_analysis', to='patient.FoodAnalysis', verbose_name='Cardápio'),
        ),
        migrations.AddField(
            model_name='substituteitem',
            name='food_substitute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substitute_food', to='food.Food', verbose_name='Alimento'),
        ),
        migrations.AddField(
            model_name='substituteitem',
            name='meal_substitute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substitute_meal', to='food.MealItem', verbose_name='Refeição'),
        ),
        migrations.AddField(
            model_name='substituteitem',
            name='unity_substitute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='substitute_unity', to='food.MeasureUnity', verbose_name='Unidade de Medida'),
        ),
        migrations.AddField(
            model_name='measure',
            name='food',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='measure_food', to='food.Food', verbose_name='Alimento'),
        ),
        migrations.AddField(
            model_name='measure',
            name='measure_unity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='measure_unity', to='food.MeasureUnity', verbose_name='Unidade de Medida'),
        ),
        migrations.AddField(
            model_name='mealitem',
            name='food_analysis',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meal_analysis', to='patient.FoodAnalysis', verbose_name='Cardápio'),
        ),
        migrations.AddField(
            model_name='mealitem',
            name='measure_unity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meal_unity', to='food.MeasureUnity', verbose_name='Unidade de Medida'),
        ),
        migrations.AddField(
            model_name='mealitem',
            name='original_food',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='meal_food', to='food.Food', verbose_name='Alimento'),
        ),
    ]
