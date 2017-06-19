from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from shareSource.models import Privilege,assignment_store,assignment
from basicInfo.models import *
from courseArrange.models import Section
from django.template import loader,context,Template
from django.http import HttpResponse
import os
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
import zipfile
import urllib.request,re
def mainForm(req):
    #TODO 获取数据部分
    #section_list = Section.objects.all()
    contents = [
        {'id': 1, 'title': 'course1', 'source_link': 'source/1', 'homework_link': 'homework/1'},
        {'id': 2, 'title': 'course2', 'source_link': 'source/2', 'homework_link': 'homework/2'},
        {'id': 3, 'title': 'course3', 'source_link': 'source/3', 'homework_link': 'homework/3'},
    ]
    #contents=[]
    #for onesection in section_list:
    #    newcontents={'id': onesection.course_id, 'title': onesection.course.title,
    #                'source_link':'source/%i'%onesection.id ,'homework_link': 'homework/%i'%onesection.id}
    #    contents.append(newcontents)
    return render(req, 'mainForm.html', {'content': contents})

def sourceForm(req, section_id):
    return render(req, 'souceForm.html', {"section_id": section_id})

def homeworkForm(req, section_id):
    return testuiforteacher(req,section_id)
# Create your views here.



#==========================================================================================================================
def testhw(req,section_id):
    if req.method == 'POST':
        if req.POST['Acontent'] == "" or req.POST['Addl'] == "" or req.POST['Arefer'] == ""  :
            return render(req,'window1.html')
        else :
            Aassignment = assignment(info=req.POST['Acontent'],ddl=req.POST['Addl'],reference=req.POST['Arefer'],courseid=section_id)
            Aassignment.save()
            return render(req,'window2.html')
    return render(req,"hw.html",{'Cid':section_id})

def testuiforstudent(req,section_id):
    Aassignment = assignment.objects.filter(courseid=section_id)
    return render(req,"ui.html",{'allob':Aassignment})

def testuiforteacher(req,section_id):
    Aassignment = assignment.objects.filter(courseid=section_id)
    return render(req,"ui2.html",{'allob':Aassignment})

def testhwforstudent(req,section_id,Aid):
    Aassignment = assignment.objects.get(id=Aid)
    if req.method == 'POST':
        myFile =req.FILES.get('myfile')
        if not myFile:
            return HttpResponse("no files for upload!")
        filepath = "D:\\uploadtest\\"+Aid+"\\"
        if os.path.exists(filepath) == 0:
            os.mkdir(filepath)
        destination = open(os.path.join(filepath,myFile.name),'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        return render(req,'window5.html')
    return render(req,"hwforstudent.html",{'ob':Aassignment})


def testhwforteacher(req,section_id,Aid):
    Aassignment = assignment.objects.get(id=Aid)
    if req.method == 'POST':
        if req.POST['Acontent'] == "" or req.POST['Addl'] == "" or req.POST['Arefer'] == ""  :
            return render(req,'window1.html')
        else :
            Aassignment.info=req.POST['Acontent']
            Aassignment.ddl=req.POST['Addl']
            Aassignment.reference=req.POST['Arefer']
            Aassignment.save()
            return render(req,'window3.html')
    return render(req,"hwforteacher.html",{'ob':Aassignment})

def testhwdel(req,section_id,Aid):
    assignment.objects.get(id=Aid).delete()

    return render(req,'window4.html')

def testdownload(req,section_id,Aid):
    #f = zipfile.ZipFile('allhomework.zip', 'w', zipfile.ZIP_DEFLATED)
   # startdir = "d:\\uploadtest\\"+Aid+"\\"
   # for dirpath, dirnames, filenames in os.walk(startdir):
    #    for filename in filenames:
    #        f.write(os.path.join(dirpath, filename))
   # f.write('D:\\uploadtest\\5\\10 Overloaded Operators.ppt')

   # f.close()

  #  os.chdir(r'd:')
  #  data = urllib.request.urlopen("d:\\uploadtest\\"+Aid+"\\"+'allhomework.zip').read()
  #  with open('download.zip', 'wb') as perunit:
  #      perunit.write(data)
    return HttpResponse('test')

def idjudge(req,section_id):
    return render(req, 'windowfortest.html')