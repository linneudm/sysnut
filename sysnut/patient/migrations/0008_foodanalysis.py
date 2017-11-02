# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-31 03:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_auto_20171030_1333'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodAnalysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='Descri\xe7\xe3o')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('update_at', models.DateTimeField(auto_now_add=True, verbose_name='Atualizado em')),
                ('published', models.BooleanField()),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysis_consultation', to='patient.Consultation', verbose_name='Consulta')),
            ],
        ),
    ]
