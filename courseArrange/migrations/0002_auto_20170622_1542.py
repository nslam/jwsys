# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-06-22 07:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basicInfo', '0013_classroom_type'),
        ('courseArrange', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCandidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField()),
                ('classroom_type', models.CharField(max_length=100)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.Course')),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.Instructor')),
            ],
        ),
        migrations.RemoveField(
            model_name='coursecandiate',
            name='course',
        ),
        migrations.RemoveField(
            model_name='coursecandiate',
            name='instructor',
        ),
        migrations.RemoveField(
            model_name='prereq',
            name='course',
        ),
        migrations.RemoveField(
            model_name='prereq',
            name='precourse',
        ),
        migrations.RemoveField(
            model_name='instructorbusytime',
            name='time_slot',
        ),
        migrations.AddField(
            model_name='instructorbusytime',
            name='day',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instructorbusytime',
            name='end_time',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='instructorbusytime',
            name='start_time',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CourseCandiate',
        ),
        migrations.DeleteModel(
            name='Prereq',
        ),
    ]
