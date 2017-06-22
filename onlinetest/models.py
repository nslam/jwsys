
# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Paper(models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey('basicInfo.Course', null=True, on_delete=models.SET_NULL)
    instructor = models.ForeignKey('basicInfo.Instructor', null=True, on_delete=models.SET_NULL)
    MAYDIFFI = (
        ('e','Easy'),
        ('m','Middle'),
        ('h','Hard'),
        )
    difficulty = models.CharField(max_length=1,choices=MAYDIFFI)
    MAYSTATUS = (
        ('o','open'),
        ('c','closed'),
        )
    status = models.CharField(max_length=1,choices=MAYSTATUS)
    limit_time = models.IntegerField()

class Question(models.Model):
    course = models.ForeignKey('basicInfo.Course', null=True, on_delete=models.SET_NULL)
    instructor = models.ForeignKey('basicInfo.Instructor', null=True, on_delete=models.SET_NULL)
    MAYBETYPE = (
        ('xz','C'),
        ('pd','P'),
        )
    q_type = models.CharField(max_length=2,choices=MAYBETYPE)
    title = models.CharField(max_length=400)
    MAYBESTATU = (
        ('o','open'),
        ('c','closed'),
        )
    status = models.CharField(max_length=1,choices=MAYBESTATU)
    answer = models.CharField(max_length=1)
    MAYDIFFI = (
        ('e','Easy'),
        ('m','Middle'),
        ('h','Hard'),
        )
    choice1 = models.CharField(max_length=400, null=True)
    choice2 = models.CharField(max_length=400, null=True)
    choice3 = models.CharField(max_length=400, null=True)
    choice4 = models.CharField(max_length=400, null=True)
    difficulty = models.CharField(max_length=1,choices=MAYDIFFI)
    test_point = models.CharField(max_length=50)
    paper = models.ManyToManyField(Paper)

class Sheet(models.Model):
    student = models.ForeignKey('basicInfo.Student', on_delete=models.CASCADE)
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    up_time = models.DateTimeField(auto_now=True)
    tot_mark = models.IntegerField(null=True)
    xz_mark = models.IntegerField(null=True)
    pd_mark = models.IntegerField(null=True)

class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE)
    ans = models.CharField(max_length=1)
    mark = models.IntegerField()
	
	