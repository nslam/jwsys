from django.db import models
from django.contrib.auth.models import User
from basicInfo.models import Instructor, Course, Classroom, TimeSlot

# Create your models here.


class Section(models.Model):
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    max_number = models.IntegerField()


class SecTimeClassroom(models.Model):
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    time_slot = models.ForeignKey(TimeSlot, null=True, on_delete=models.SET_NULL)
    classroom = models.ForeignKey(Classroom, null=True, on_delete=models.SET_NULL)


class Teaches(models.Model):
    instructor = models.ForeignKey(Instructor, null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)


class InstructorBusyTime(models.Model):
    instructor = models.ForeignKey(Instructor, null=True, on_delete=models.SET_NULL)
    day = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()


class CourseCandidate(models.Model):
    instructor = models.ForeignKey(Instructor, null=True, on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    capacity = models.IntegerField()
    classroom_type = models.CharField(max_length=100)


