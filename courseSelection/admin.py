from django.contrib import admin
from .models import *
from django.contrib import admin

admin.site.register([MajorCourse,Curriculum,CurriculumDemand,Selection,SelectionTime,Constants])
# Register your models here.
