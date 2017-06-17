# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-12 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0007_auto_20170609_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='instructor',
            name='birthday',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='instructor',
            name='nickName',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='manager',
            name='birthday',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='manager',
            name='nickName',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='birthday',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='student',
            name='nickName',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]