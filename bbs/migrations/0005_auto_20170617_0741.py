# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 07:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0004_remove_notice_title'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reply',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='reply',
            name='layer',
        ),
    ]