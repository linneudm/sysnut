# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 14:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_auto_20171029_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='energycalc',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='consultation_energcalc', to='patient.EnergyCalc', verbose_name='Calculos Energ\xe9ticos'),
        ),
        migrations.AlterField(
            model_name='energycalc',
            name='height',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Altura (cm)'),
        ),
    ]
