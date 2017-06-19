from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect,StreamingHttpResponse
from shareSource.models import Privilege,assignment_store,assignment,file
from basicInfo.models import *
from courseArrange.models import Section
from django.template import loader,context,Template
from django.http import HttpResponse
import os
import datetime
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
import zipfile
import urllib.request,re
def mainForm(req):
    #TODO 获取数据部分
    #section_list = Section.objects.all()
    # user = User.objects.get(id=request.user.id)
    # type = getType(user)
    # section_list = []
    # if type == 'Manager':
    #     useid = user.manager.user_id
    #     section_list = Section.objects.all()
    # else:
    #     if type == 'Student':
    #         useid = user.student.user_id
    #     elif type == 'Instructor':
    #         useid = user.instructor.user_id
    #     for i in Privilege.objects.filter(userid=useid):
    #         section_list.append(i.section)
    contents = [
        {'id': 1, 'title': 'course1', 'source_link': 'sourceForm/1', 'homework_link': 'homework/1'},
        {'id': 2, 'title': 'course2', 'source_link': 'sourceForm/2', 'homework_link': 'homework/2'},
        {'id': 3, 'title': 'course3', 'source_link': 'sourceForm/3', 'homework_link': 'homework/3'},
    ]
    #contents=[]
    #for onesection in section_list:
    #    newcontents={'id': onesection.course_id, 'title': onesection.course.title,
    #                'source_link':'source/%i'%onesection.id ,'homework_link': 'homework/%i'%onesection.id}
    #    contents.append(newcontents)
    return render(req, 'mainForm.html', {'content': contents})

def sourceForm(req, section_id):
    return seefile(req,section_id)

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
        filepath = "D:\\sharesource\\homework\\"+Aid+"\\"
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

def seefile(req,section_id):
    if req.method == 'POST':
        print('successful')
        myFile =req.FILES.get('myfile')
        if not myFile:
            return HttpResponse("no files for upload!")
        filepath = "D:\\sharesource\\source\\"+section_id+"\\"
        if os.path.exists(filepath) == 0:
            os.mkdir(filepath)
        destination = open(os.path.join(filepath,myFile.name),'wb+')
        for chunk in myFile.chunks():
            destination.write(chunk)
        destination.close()
        f1 = file(course_id=section_id,file_id=10000,file_name=myFile.name,file_path=filepath,update_time=datetime.datetime.now(),download_times=0,flag=10000,flag_top=0)
        if (file.objects.count()!=0):
            a = file.objects.latest('file_id')
            f1.file_id=(a.file_id+1)
        f1.save()
        return render(req,'window5.html')


    Ffile = file.objects.all().filter(course_id=section_id).order_by("-flag_top","-file_id")

    return render(req,"souceForm.html",{'file':Ffile,'sid':section_id})

def filedel(req,section_id,fid):
    file.objects.get(id=fid).delete()
    return render(req, 'window6.html')

def filetop(req,section_id,fid):
    b = file.objects.latest('flag_top')
    n=b.flag_top+1
    file.objects.filter(id=fid).update(flag_top=n)
    return render(req, 'window7.html')

def fileuntop(req,section_id,fid):
    file.objects.filter(id=fid).update(flag_top=0)
    return render(req, 'window8.html')


def filedownload(req,section_id,fid):
    f = file.objects.get(id=fid)
    file.objects.filter(id=fid).update(download_times=f.download_times+1)
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