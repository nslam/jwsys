from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from shareSource.models import Privilege
from basicInfo.models import *
from courseArrange.models import Section

def mainForm(req):
    #TODO 获取数据部分
    section_list = Section.objects.all()
    contents=[]
    for onesection in section_list:
        newcontents={'id': onesection.course_id, 'title': onesection.course.title,
                    'source_link':'source/%i'%onesection.id ,'homework_link': 'homework/%i'%onesection.id}
        contents.append(newcontents)
    return render(req, 'mainForm.html', {'content': contents})

def sourceForm(req, section_id):
    return render(req, 'souceForm.html', {"section_id": section_id})

def homeworkForm(req, section_id):
    return render(req, 'homeworkForm.html', {"section_id": section_id})
# Create your views here.
