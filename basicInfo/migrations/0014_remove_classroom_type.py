# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-22 11:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0013_classroom_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='type',
        ),
    ]
