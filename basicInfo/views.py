from django.shortcuts import render, render_to_response
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import math


def getGradePoint(grade):
    if grade >= 95:
        return 5
    elif grade < 60:
        return 0
    elif grade < 95 and grade >= 92:
        return 4.8
    else:
        return 4.8 - math.ceil(92 - grade) / 3 * 0.3


def getType(user):
    try:
        student = user.student
        ret = 'Student'
    except:
        try:
            instructor = user.instructor
            ret = 'Instructor'
        except:
            try:
                manager = user.manager
                ret = 'Manager'
            except:
                ret = 'none'
    return ret


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
    if type == 'Student':
        try:
            test = user.student
        except:
            return render(request, 'login.html', {'status': 'You are not a student!'})
    if type == 'Instructor':
        try:
            test = user.instructor
        except:
            return render(request, 'login.html', {'status': 'You are not a instructor!'})
    # if type == 'Manager':
    #     try:
    #         test = user.manager
    #     except:
    #         return render(request, 'login.html', {'status': 'You are not a manager!'})
    auth.login(request=request, user=user)
    # Check type !!!!! Here I do not check that....
    if type == 'Student':
        return render(request, 'student_main.html', {'username': username})
    elif type == 'Instructor':
        return render(request, 'instructor_main.html', {'username': username})
    elif type == 'Manager':
        return render(request, 'manager_main.html', {'username': username})


@login_required
def setPassword(request):
    if request.method == 'GET':
        return render(request, 'changepwd.html', {'status': 'true'})
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
        return render(request, 'changepwd.html', {'status': status})


@login_required
def changeInfo(request):
    ret = {}
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type == 'Student':
        item = user.student
    elif type == 'Instructor':
        item = user.instructor
    elif type == 'Manager':
        item = user.manager
    if request.method == 'GET':
        ret['phoneNumber'] = item.phone_number
        ret['address'] = item.address
        ret['gender'] = item.gender
        ret['userId'] = user.id
        if type == 'Student':
            ret['major'] = item.major.name
            ret['dept'] = item.major.department
        else:
            ret['major'] = None
            ret['dept'] = None
        return render(request, 'personal_info.html', ret)
    else:
        item.address = request.POST['address']
        item.phone_number = request.POST['phoneNumber']
        item.save()
        return HttpResponse('success')


@login_required
def stuGradeQuery(request):
    user = request.user
    type = getType(user)
    if type != 'Student':
        return HttpResponse('You are not a student!')
    takes = Takes.objects.filter(student=user.student)
    ret = []
    for take in takes:
        ret.append({'title': take.section.course.title, 'courseNumber': take.section.course.course_number,
                    'credit': take.section.course.credits, 'grade': take.score,
                    'gradePoint': getGradePoint(take.score)})
    return render(request, 'student/stu_grade_query.html', ret)


@login_required
def stuGradeAnalysis(request):
    user = request.user
    type = getType(user)
    if type != 'Student':
        return HttpResponse('You are not a student!')
    takes = Takes.objects.filter(student=user.student)
    ret = {}
    gp = 0
    totalCredits = 0
    for take in takes:
        gp += getGradePoint(take.score) * take.section.course.credits
        totalCredits += take.section.course.credits
    ret['gp'] = gp
    if totalCredits == 0:
        ret['gpa'] = 0
    else:
        ret['gpa'] = gp / totalCredits
    return render(request, 'student/stu_grade_analysis.html', ret)


@login_required
def addCourse(request):
    user = User.objects.get(request.user.id)
    type = getType(user)
    if type != 'Instructor':
        return HttpResponse('You are not a instructor!')
    if request.method == 'GET':
        return render(request, 'instructor/instructor_course_apply.html', {'dept': user.instructor.department})
    else:
        course = Course.objects.create()
        course.course_number = str(course.id)
        course.title = request.POST['title']
        course.credits = request.POST['credits']
        course.week_hour = request.POST['weekHour']
        course.method = request.POST['method']
        course.save()
        return HttpResponse('Success')


@login_required
def queryCourse(request):
    ret = []
    user = User.objects.get(request.user.id)
    type = getType(user)
    if type != 'Instructor':
        return HttpResponse('You are not a instructor!')
    teaches = Teaches.objects.filter(instructor=user.instructor.id)
    for teach in teaches:
        course = teach.section.course
        ret.append({
            'title': course.title,
            'method': course.method,
            'courseNumber': course.course_number,
            'credit': course.credits,
            'weekHour': course.week_hour
        })
    render(request, 'instructor/instructor_course_query.html', ret)


@login_required
def gradeInput(request):
    ret = []
    user = User.objects.get(request.user.id)
    type = getType(user)
    if type != 'Instructor':
        return HttpResponse('You are not a instructor!')
    teaches = Teaches.objects.filter(instructor=user.instructor.id)
    for teach in teaches:
        course = teach.section.course
        ret.append({
            'sectionId': teach.section.id,
            'title': course.title,
            'courseNumber': course.course_number,
            'credit': course.credits
        })
    render(request, 'instructor/instructor_course_query.html', ret)


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

#
#
# @login_required
# def inputScore(request):
#     if request.user.instructor is None:
#         return HttpResponse('You are not a instrctor!')
#     section = section.Objects.get(id=request.POST['sectionId'])
#     students = section.student_set.all()
#     for student in students:
#         insert
#         record
#         to
#         Takes
#     return HttpResponse('success')
#
#
# @login_required
# def teacherGetScore(request):
#     if request.user.instructor is None:
#         return HttpResponse('You are not a instrctor!')
#     section = section.Objects.get(id=request.POST['sectionId'])
#     students = section.student_set.all()
#     ret = []
#     for student in students:
#         ret.append({'id': student.id, 'score': student.score})
#     return JsonResponse(ret)
#
# #
# # @login_required
# # def changeScore(request):
# #     if request.user.instructor is None:
# #         return HttpResponse('You are not a instrctor!')
# #     if request.user.check_password(request.POST['password']) is False:
# #         return HttpResponse('Password is wrong!')
# #     section = section.Objects.get(id=request.POST['sectionId'])
# #     student = request.POST['studentId']
# #     student.score = request.POST['score']
# #     return HttpResponse('success')
#
#
# @login_required
# def studentGetScore(request):
#     if request.user.student is None:
#         return HttpResponse('You are not a student!')
#     student = request.user.student
#     sections = student.section_set.all()
#     for section in sections:
#         ret.append({'sectionId': section.id, 'score': section.score})
#     return JsonResponse(ret)


# @login_required
# def analyzeScore(request):
#     student = request.user.student
#     scores = student.score.all()
#     ret = [avg_score, GP, GPA, Rank, Credit_earned, Credit_required]
#     return JsonResponse(ret)
