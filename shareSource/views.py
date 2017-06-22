from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, StreamingHttpResponse
from django.template import loader, context, Template, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, render

from shareSource.models import Privilege, assignment_store, assignment, file
from basicInfo.models import *
from basicInfo.views import getType
from courseArrange.models import Section, Teaches

import os
import datetime
import zipfile
import urllib.request, re

@login_required
def mainForm(req):
    #建立需要的文件夹
    folderpath = 'shareSource\\homework'
    exist = os.path.exists(folderpath)
    if not exist:
        os.mkdir(folderpath)
    folderpath = 'shareSource\\source'
    exist = os.path.exists(folderpath)
    if not exist:
        os.mkdir(folderpath)
    #身份检查
    user = User.objects.get(id=req.user.id)
    type = getType(user)
    section_list = []
    if type == 'Manager':
        section_list = Section.objects.all()
    else:
        if type == 'Student':
            for i in Takes.objects.fliter(student=user.student):
                section_list.append(i.section)
        elif type == 'Instructor':
            for i in Teaches.objects.fliter(instructor=user.instructor):
                section_list.append(i.section)
    #test data
    #contents = [
    #    {'id': 1, 'title': 'course1', 'source_link': 'sourceForm/1', 'homework_link': 'homework/1'},
    #    {'id': 2, 'title': 'course2', 'source_link': 'sourceForm/2', 'homework_link': 'homework/2'},
    #    {'id': 3, 'title': 'course3', 'source_link': 'sourceForm/3', 'homework_link': 'homework/3'},
    #]
    contents=[]
    for onesection in section_list:
        newcontents={'id': onesection.id, 'title': onesection.course.title,
                    'source_link':'source/%i'%onesection.id ,'homework_link': 'homework/%i'%onesection.id}
        contents.append(newcontents)
    return render(req, 'mainForm.html', {'content': contents})

def sourceForm(req, section_id):
    return seefile(req,section_id)

#==========================================================================================================================
def CheckStu(req,sid):
    if getType(req.user) == 'Student' and Takes.objects.fliter(student=req.user.student, section_id=sid).count() != 0:
        return 1
    else:
        return 0
def CheckIns(req,sid):
    if getType(req.user) == 'Instructor' and Teaches.objects.fliter(instructor=req.user.instructor, section_id=sid).count() != 0:
        return 1
    else:
        return 0

@login_required
def hw(req,s_id):
    if CheckIns(req,s_id) == 0 and CheckStu(req,s_id) == 0:
        return HttpResponse("You have no rights")
    if req.method == 'POST':
        if req.POST['Acontent'] == "" or req.POST['Addl'] == "" or req.POST['Arefer'] == ""  :
            return render(req,'window1.html')
        else :
            Aassignment = assignment(info=req.POST['Acontent'],ddl=req.POST['Addl'],reference=req.POST['Arefer'],courseid=s_id)
            Aassignment.save()
            return render(req,'window2.html')
    return render(req,"hw.html",{'Cid':s_id})

@login_required
def uiforstudent(req,s_id):
    if CheckStu(req,s_id) == 0:
        return HttpResponse("You have no rights")
    Aassignment = assignment.objects.fliter(courseid=s_id)
    return render(req,"ui.html",{'allob':Aassignment})

@login_required
def uiforteacher(req,s_id):
    if CheckIns(req,s_id) == 0:
        return HttpResponse("You have no rights")
    Aassignment = assignment.objects.fliter(courseid=s_id)
    return render(req,"ui2.html",{'allob':Aassignment})

@login_required
def hwforstudent(req,s_id,Aid):
    if CheckStu(req,s_id) == 0:
        return HttpResponse("You have no rights")
    Aassignment = assignment.objects.get(id=Aid)
    if req.method == 'POST':
        myFile =req.FILES.get('myfile')
        if not myFile:
            return HttpResponse("no files for upload!")
        filepath = "shareSource\\homework\\"+Aid+"\\"
        if os.path.exists(filepath) == 0:
            os.mkdir(filepath)
        destination = open(os.path.join(filepath,myFile.name),'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        newhw=assignment_store(assignmentid=Aid,file_name=myFile.name)
        newhw.save()
        return render(req,'window5.html')
    return render(req,"hwforstudent.html",{'ob':Aassignment})

@login_required
def hwforteacher(req,s_id,Aid):
    if CheckIns(req,s_id) == 0:
        return HttpResponse("You have no rights")
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

@login_required
def hwdel(req,s_id,Aid):
    if CheckIns(req,s_id) == 0:
        return HttpResponse("You have no rights")
    assignment.objects.get(id=Aid).delete()
    return render(req,'window4.html')

@login_required
def hwdownload(req,s_id,Aid):
    if CheckIns(req,s_id) == 0:
        return HttpResponse("You have no rights")
    filepath="shareSource\\homework\\" + Aid + "\\"+"hw.zip"
    f = zipfile.ZipFile(filepath, 'w')
    allhw=assignment_store.objects.fliter(assignmentid=Aid)
    for eachhw in allhw:
        f.write("shareSource\\homework\\" + Aid + "\\"+eachhw.file_name)
    f.close()
    response = StreamingHttpResponse(readFile(filepath))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format('hw.rar')
    return response

@login_required
def idjudge(req,section_id):
    whoisthis=''
    if getType(req.user) == 'Student':
        whoisthis = 'student'
    else:
        whoisthis = 'teacher'
    if whoisthis =='teacher':
        return HttpResponseRedirect('teacher')
    else:
        return HttpResponseRedirect('student')

@login_required
def seefile(req,section_id):
    if req.method == 'POST':
        print('successful')
        myFile =req.FILES.get('myfile')
        if not myFile:
            return HttpResponse("no files for upload!")
        filepath = "shareSource\\source\\"+section_id+"\\"
        if os.path.exists(filepath) == 0:
            os.mkdir(filepath)
        destination = open(os.path.join(filepath,myFile.name),'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        f1 = file(course_id=section_id,file_id=10000,file_name=myFile.name,file_path=filepath,update_time=datetime.datetime.now(),download_times=0,flag=10000,flag_top=0)
        #user_id=req.user.id)
        if (file.objects.count()!=0):
            a = file.objects.latest('file_id')
            f1.file_id=(a.file_id+1)
        f1.save()
        return render(req,'window5.html')

    Ffile = file.objects.all().fliter(course_id=section_id and section_id in Section.objects.Course.objects.value("course_number")).order_by("-flag_top","-file_id")

    return render(req,"souceForm.html",{'file':Ffile,'sid':section_id})

@login_required
def filedel(req,section_id,fid):
    f=file.object.get(id=fid)
    user = User.objects.get()
    type = getType(user)
    if(req.user.id==f.user_id or type=='Instructor'):
        file.objects.get(id=fid).delete()
        return render(req, 'window6.html')
    else:
        return render(req,'window9,html')

@login_required
def filetop(req,section_id,fid):
    b = file.objects.latest('flag_top')
    n=b.flag_top+1
    user = User.objects.get()
    type=getType(user)
    if(type=='Student'):
        return render(req,'window10.html')
    else:
        file.objects.fliter(id=fid).update(flag_top=n)
        return render(req, 'window7.html')

@login_required
def fileuntop(req,section_id,fid):
    user = User.objects.get()
    type=getType(user)
    if(type=='Student'):
        return render(req,'window10.html')
    else:
        file.objects.fliter(id=fid).update(flag_top=0)
        return render(req, 'window8.html')

@login_required
def filedownload(req,section_id,fid):
    f = file.objects.get(id=fid)
    file.objects.fliter(id=fid).update(download_times=f.download_times+1)
    the_file_name=f.file_name
    filename=str(f.file_path)+f.file_name
    response=StreamingHttpResponse(readFile(filename))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="{0}"'.format(the_file_name)
    return response

def readFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if  c:
                yield   c
            else:
                break