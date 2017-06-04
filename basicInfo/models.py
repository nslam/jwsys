from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100)
    building = models.CharField(max_length=100)


class Major(models.Model):
    name = models.CharField(max_length=50, default='')
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_file = models.FileField(upload_to=None)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_file = models.FileField(upload_to=None)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_file = models.FileField(upload_to=None)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    tot_cred = models.IntegerField(default=0)
    major = models.ForeignKey(Major, null=True, on_delete=models.SET_NULL)
    matriculate = models.IntegerField()
    graduate = models.IntegerField()


class Course(models.Model):
    course_number = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    credits = models.IntegerField()
    week_hour = models.IntegerField()
    type = models.CharField(max_length=20)
    precourse = models.ForeignKey('Course', null=True, on_delete=models.SET_NULL)


class Log(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    event = models.TextField()


class Classroom(models.Model):
    building = models.CharField(max_length=100)
    room_number = models.IntegerField()
    capacity = models.IntegerField()
    equipment = models.ManyToManyField('Equipment')


class Section(models.Model):
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    semester = models.CharField(max_length=20)
    year = models.IntegerField()
    max_number = models.IntegerField()
    instructor = models.ForeignKey(Instructor, null=True, on_delete=models.SET_NULL)


class Takes(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    section = models.ForeignKey(Section, null=True, on_delete=models.SET_NULL)
    score = models.IntegerField()


class TimeSlot(models.Model):
    day = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class Equipment(models.Model):
    name = models.CharField(max_length=100)
