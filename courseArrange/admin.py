from django.contrib import admin
from .models import *
from django.contrib import admin

admin.site.register([Section,Teaches,SecTimeClassroom,InstructorBusyTime,CourseCandiate])