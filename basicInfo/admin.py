from django.contrib import admin
from .models import *
from django.contrib import admin


class LogAdmin(admin.ModelAdmin):
    readonly_fields = ('event', 'time')


admin.site.register(Log, LogAdmin)
admin.site.register([Student, Instructor, Manager, Course, Takes, Major, Classroom, Department])
# Register your models here.
