from django.db import models
from django.contrib.auth.models import User
from basicInfo.models import Department, Major, Instructor, Course, Classroom, Equipment, TimeSlot


class Section(models.Model):
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    max_number = models.IntegerField()


class Teaches(models.Model):
    instructor = models.ForeignKey(Instructor, null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)


class Prereq(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='allPreCourses')
    precourse = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subCourses')


class SecTimeClassroom(models.Model):
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    time_slot = models.ForeignKey(TimeSlot, null=True, on_delete=models.SET_NULL)
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)


class InstructorBusyTime(models.Model):
    instructor = models.ForeignKey(Instructor, null=True, on_delete=models.SET_NULL)
    time_slot = models.ForeignKey(TimeSlot, null=True, on_delete=models.SET_NULL)


class CourseCandiate(models.Model):
    instructor = models.ForeignKey(Instructor, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)

