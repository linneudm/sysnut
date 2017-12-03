# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-03 13:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_auto_20171203_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='BiochemicalExam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, verbose_name='Descricao')),
                ('condiction', models.CharField(choices=[('Alto', 'Alto'), ('Normal', 'Normal'), ('Baixo', 'Baixo')], default=None, max_length=10, verbose_name='Condição')),
            ],
        ),
        migrations.AddField(
            model_name='consultation',
            name='biochemical',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='consultation_biochemical', to='patient.BiochemicalExam', verbose_name='Exame Bioquímico'),
            preserve_default=False,
        ),
    ]
