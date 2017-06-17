# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 11:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courseArrange', '0001_initial'),
        ('basicInfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Takes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courseArrange.Section')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basicInfo.Student')),
            ],
        ),
    ]
