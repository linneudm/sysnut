# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-06 03:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0009_auto_20171205_2352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodanalysis',
            name='guidanceaux',
        ),
        migrations.AddField(
            model_name='foodanalysis',
            name='guidanceaux',
            field=models.ManyToManyField(related_name='analysis_guidanceaux', to='patient.GuidanceAux', verbose_name='OrientaçãoAux'),
        ),
    ]
