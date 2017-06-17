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
