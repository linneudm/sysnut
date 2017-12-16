# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-16 04:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0018_auto_20171216_0058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='vitamin',
        ),
        migrations.AddField(
            model_name='consultation',
            name='vitamin',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='consultation_vitamin', to='patient.Vitamin', verbose_name='Deficiência Vitamínica'),
            preserve_default=False,
        ),
    ]
