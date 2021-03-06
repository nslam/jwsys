# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-18 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0008_auto_20170612_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='credits',
            field=models.FloatField(),
        ),
        migrations.RemoveField(
            model_name='course',
            name='precourse',
        ),
        migrations.AddField(
            model_name='course',
            name='precourse',
            field=models.ManyToManyField(null=True, to='basicInfo.Course'),
        ),
        migrations.AlterField(
            model_name='student',
            name='tot_cred',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='takes',
            name='score',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='end_time',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='start_time',
            field=models.IntegerField(),
        ),
    ]
