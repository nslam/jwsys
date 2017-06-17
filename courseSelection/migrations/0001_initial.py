# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 07:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courseArrange', '0001_initial'),
        ('basicInfo', '0007_auto_20170609_1953'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.Course')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.Student')),
            ],
        ),
        migrations.CreateModel(
            name='CurriculumDemand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compulsory', models.IntegerField()),
                ('elective', models.IntegerField()),
                ('public', models.IntegerField()),
                ('major', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.Major')),
            ],
        ),
        migrations.CreateModel(
            name='MajorCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compulsory', models.BooleanField()),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.Course')),
                ('major', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.Major')),
            ],
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selection_round', models.IntegerField()),
                ('select_time', models.TimeField()),
                ('drop_time', models.TimeField(null=True)),
                ('priority', models.IntegerField()),
                ('condition', models.IntegerField()),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='courseArrange.Section')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basicInfo.Student')),
            ],
        ),
        migrations.CreateModel(
            name='SelectionTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('semester', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('selection_round', models.IntegerField()),
            ],
        ),
    ]