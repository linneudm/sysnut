# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-06 02:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_auto_20171205_2322'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guidanceaux',
            old_name='message',
            new_name='message2',
        ),
        migrations.RenameField(
            model_name='guidanceaux',
            old_name='show',
            new_name='show2',
        ),
    ]
