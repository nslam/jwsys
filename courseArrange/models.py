from django.db import models
from django.contrib.auth.models import User



class Section(models.Model):
    course = models.ForeignKey('basicInfo.Course', null=True, on_delete=models.SET_NULL)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    max_number = models.IntegerField()


class Teaches(models.Model):
    instructor = models.ForeignKey('basicInfo.Instructor', null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)


class Prereq(models.Model):
    course = models.ForeignKey('basicInfo.Course', on_delete=models.CASCADE, related_name='allPreCourses')
    precourse = models.ForeignKey('basicInfo.Course', on_delete=models.CASCADE, related_name='subCourses')


class SecTimeClassroom(models.Model):
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    time_slot = models.ForeignKey('basicInfo.TimeSlot', null=True, on_delete=models.SET_NULL)
    classroom = models.ForeignKey('basicInfo.Classroom', null=True, on_delete=models.SET_NULL)


class InstructorBusyTime(models.Model):
    instructor = models.ForeignKey('basicInfo.Instructor', null=True, on_delete=models.SET_NULL)
    time_slot = models.ForeignKey('basicInfo.TimeSlot', null=True, on_delete=models.SET_NULL)
    day = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()


class CourseCandiate(models.Model):
    instructor = models.ForeignKey('basicInfo.Instructor', null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey('basicInfo.Course', null=True, on_delete=models.SET_NULL)
    capacity = models.IntegerField()
    classroom_type = models.IntegerField()