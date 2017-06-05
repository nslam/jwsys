from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    logs=Log.objects.filter(event__contains=request.POST['username'])
    if login too frequent:
        return HttpResponse('Log in too frequent!')
    pass
    if username is None:
        return HttpResponse('username cannot be none!')
    if password is None:
        return HttpResponse('Password cannot be none!')
    user = authenticate(username=username, password=password)
    if user is None:
        return HttpResponse('Password is not correct!')
    return HttpResponse('Login successed!')


@login_required
def setPassword(request):
    flag = request.user.check_password(request.POST['password'])
    if flag is False:
        return HttpResponse('Password is wrong!')
    request.user.set_password(request.POST['newPassword'])
    return HttpResponse('Password changed!')


@login_required
def changeInfo(request):
    if request.user.student is not None:
        info = request.user.student
    elif request.user.instructor is not None:
        info = request.user.instructor
    elif request.user.manager is not None:
        info = request.user.manager
    info.address = request.POST['address']
    info.phone_number = request.POST['phone_number']
    info.save()
    return HttpResponse('success')


@login_required
def addCourse(request):
    if request.user.instructor is None:
        return HttpResponse('You are not a instructor!')
    instructor = request.user.instructor
    info = request.POST['info']
    if Course.objects.get(info=info):
        return HttpResponse('The course already exists!')
    course = Course()
    course.info = info
    course.save()
    return HttpResponse('success')


@login_required
def changeCourse(request):
    if request.user.manager is None:
        return HttpResponse('You are not a manager!')
    if request.user.check_password(request.POST['password']) is False:
        return HttpResponse('Password is wrong!')
    manager = request.user.manager
    course = Course.objects.get(name=request.POST['courseName'])
    course.info = request.POST['info']
    course.save()
    return HttpResponse('success')


@login_required
def dropCourse(request):
    if request.user.manager is None:
        return HttpResponse('You are not a manager!')
    if request.user.check_password(request.POST['password']) is False:
        return HttpResponse('Password is wrong!')
    manager = request.user.manager
    course = Course.objects.get(name=request.POST['courseName'])
    course.delete()


@login_required
def addUser(request):
    if request.user.manager is None:
        return HttpResponse('You are not a manager!')
    if request.user.check_password(request.POST['password']) is False:
        return HttpResponse('Password is wrong!')
    if request.POST['identity'] == 'instructor':
        if User.objects.get(info=info):
            return HttpResponse('User already exists!')
        user = User()
        if request['info'] is not valid:
            return HttpResponse('Information is not valid!')
        user.info = request['info']
        user.save()
    elif request.POST['identity'] == 'student':
        if User.objects.get(info=info):
            return HttpResponse('User already exists!')
        user = User()
        if request['info'] is not valid:
            return HttpResponse('Information is not valid!')
        user.info = request['info']
        user.save()
    return HttpResponse('success')


@login_required
def searchLog(request):
    if request.user.manager is None:
        return HttpResponse('You are not a manager!')
    if request.user.check_password(request.POST['password']) is False:
        return HttpResponse('Password is wrong!')
    logs=Log.objects.all()
    ret=[]
    for log in logs:
        ret.append(log)
    return JsonResponse(ret)
