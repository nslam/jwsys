from django.contrib import admin
from .models import *
from django.contrib import admin

admin.site.register([Student, Instructor, Manager, Course, Takes, Log])
# Register your models here.
