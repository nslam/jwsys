from django.db import models

class Privilege(models.Model):
    userid = models.IntegerField(default=0)
    sectionid = models.IntegerField(default=0)
    status = models.CharField(max_length=1)

# Create your models here.
