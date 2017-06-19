from django.db import models
from courseArrange.models import Section

class Privilege(models.Model):
    STATUS = (
        ('s', 'student'),
        ('t', 'teacher'),
        ('m', 'manager'),
    )
    userid = models.IntegerField(default=0)
    sectionid = models.IntegerField(default=0)
    #sectionid=models.ForeignKey(Section , on_delete = models.CASCADE)
    status = models.CharField(max_length=1 , choices=STATUS)
# Create your models here.



class assignment(models.Model):
     info=models.TextField()
     ddl=models.DateField()
     reference=models.CharField(max_length=30)
     courseid=models.CharField(max_length=15)
     comment=models.FileField(upload_to='uploads/assignment/')

class assignment_store(models.Model):
     assignmentid=models.CharField(max_length=15)
     studentid=models.CharField(max_length=15)
     file_path=models.FileField(upload_to='uploads/assignment/')
     status=models.CharField(max_length=15)