from django.shortcuts import render, render_to_response
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def index(request):
    status = 'true'
    return render(request, 'login.html', {'status': status})


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    type = request.POST['type']
    # logs = Log.objects.filter(event__contains=request.POST['username'])
    # if login too frequent:
    #     return HttpResponse('Log in too frequent!')
    # pass
    if username is None or password is None:
        status = 'User name or password cannot be none!'
        return render(request, 'login.html', {'status': status})
    user = authenticate(username=username, password=password)
    if user is None:
        status = 'Password is not correct!'
        return render(request, 'login.html', {'status': status})
    if not user.is_active:
        status = 'User is not active!'
        return render(request, 'login.html', {'status': status})
    auth.login(request=request, user=user)
    # Check type !!!!! Here I do not check that....
    if type == 'Student':
        return render(request, 'student_main.html', {'username': username})
    elif type == 'Teacher':
        return render(request, 'instructor_main.html', {'username': username })
    elif type == 'Manager':
        return render(request, 'manager_main.html', {'username': username})


@login_required
def setPassword(request):
    if request.method == 'GET':
        return render(request, 'changepwd.html', {'status':'true'})
    else:
        originPwd = request.POST['originPwd']
        newPwd = request.POST['newPwd']
        newPwdAgain = request.POST['newPwdAgain']
        flag = request.user.check_password(originPwd)
        if flag is False:
            status = 'Original password is not correct!'
        elif newPwd != newPwdAgain:
            status = 'New passwords are not same!'
        else:
            request.user.set_password(newPwd)
            request.user.save()
            status = 'Password changed successful!'
        return render(request, 'changepwd.html', {'status':status})


@login_required
def changeInfo(request):
    if request.method == 'GET':
        #Fetch info into the form & render
        return render(request, 'personal_info.html')
    else:
        if request.POST['identity'] == 'student':
            info = request.user.student
        elif request.POST['identity'] == 'instructor':
            info = request.user.instructor
        elif request.POST['identity'] == 'manager':
            info = request.user.manager
        if info is None:
            return HttpResponse('No such person!')
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
def addStudent(request):
    if request.user.manager is None:
        return HttpResponse('You are not a manager!')
    user = User.objects.get(username=request.POST['username'])
    if user is not None:
        return HttpResponse('Account already exists!')
    user = User.objects.create_user(username=request.POST['username'], password='123456')
    user.last_name = request['lastname']
    user.first_name = request['firstname']
    user.save()
    student = Student.objects.create(user=user)
    student.matriculate = request.POST['matriculate']
    student.major = request.POST['major']
    student.save()
    return HttpResponse('success')


@login_required
def addInstructor(request):
    if request.user.manager is None:
        return HttpResponse('You are not a manager!')
    user = User.objects.get(username=request.POST['username'])
    if user is not None:
        return HttpResponse('Account already exists!')
    user = User.objects.create_user(username=request.POST['username'], password='123456')
    user.last_name = request['lastname']
    user.first_name = request['firstname']
    user.save()
    Instructor.objects.create(user=user)
    return HttpResponse('success')


@login_required
def searchLog(request):
    if request.user.manager is None:
        return HttpResponse('You are not a manager!')
    if request.user.check_password(request.POST['password']) is False:
        return HttpResponse('Password is wrong!')
    logs = Log.objects.all()
    ret = []
    for log in logs:
        ret.append(log)
    return JsonResponse(ret)


@login_required
def inputScore(request):
    if request.user.instructor is None:
        return HttpResponse('You are not a instrctor!')
    section = section.Objects.get(id=request.POST['sectionId'])
    students = section.student_set.all()
    for student in students:
        insert
        record
        to
        Takes
    return HttpResponse('success')


@login_required
def teacherGetScore(request):
    if request.user.instructor is None:
        return HttpResponse('You are not a instrctor!')
    section = section.Objects.get(id=request.POST['sectionId'])
    students = section.student_set.all()
    ret = []
    for student in students:
        ret.append({'id': student.id, 'score': student.score})
    return JsonResponse(ret)


@login_required
def changeScore(request):
    if request.user.instructor is None:
        return HttpResponse('You are not a instrctor!')
    if request.user.check_password(request.POST['password']) is False:
        return HttpResponse('Password is wrong!')
    section = section.Objects.get(id=request.POST['sectionId'])
    student = request.POST['studentId']
    student.score = request.POST['score']
    return HttpResponse('success')


@login_required
def studentGetScore(request):
    if request.user.student is None:
        return HttpResponse('You are not a student!')
    student = request.user.student
    sections = student.section_set.all()
    for section in sections:
        ret.append({'sectionId': section.id, 'score': section.score})
    return JsonResponse(ret)


@login_required
def analyzeScore(request):
    student = request.user.student
    scores = student.score.all()
    ret = [avg_score, GP, GPA, Rank, Credit_earned, Credit_required]
    return JsonResponse(ret)
