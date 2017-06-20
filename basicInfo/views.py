from django.shortcuts import render, redirect, reverse, render_to_response
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from courseArrange.models import Teaches, Section
from django.utils.datastructures import MultiValueDictKeyError
import math
import operator


def getGradePoint(grade):
    if grade >= 95:
        return 5
    elif grade < 60:
        return 0
    elif grade < 95 and grade >= 92:
        return 4.8
    else:
        return 4.8 - math.ceil(92 - grade) / 3 * 0.3


def stuMain(request):
    username = request.user
    return render(request, 'student_main.html', {'username': username})


def instructorMain(request):
    username = request.user
    return render(request, 'instructor_main.html', {'username': username})


def managerMain(request):
    username = request.user
    return render(request, 'manager_main.html', {'username': username})


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


def logCreate(event):
    log = Log.objects.create()
    log.event = event
    log.save()


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
        logCreate('login ' + str(username) + 'failed (pwd none)')
        return render(request, 'login.html', {'status': status})
    user = authenticate(username=username, password=password)
    if user is None:
        status = 'Password is not correct!'
        logCreate('login ' + str(username) + 'failed (pwd not correct) pwd:' + str(password))
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
            return render(request, 'login.html', {'status': 'You are not an instructor!'})
    if type == 'Manager':
        try:
            test = user.manager
        except:
            return render(request, 'login.html', {'status': 'You are not a manager!'})
    auth.login(request=request, user=user)
    # Check type !!!!! Here I do not check that....
    logCreate('login ' + str(username) + ' success!')
    if type == 'Student':
        return HttpResponseRedirect('/basicInfo/stuMain')
    elif type == 'Instructor':
        return HttpResponseRedirect('/basicInfo/instructorMain')
    elif type == 'Manager':
        return HttpResponseRedirect('/basicInfo/managerMain')


@login_required
def setPassword(request):
    if request.method == 'GET':
        return render(request, 'changepwd.html', {'status': 'true'})
    else:
        originPwd = request.POST['originPwd']
        newPwd = request.POST['newPwd']
        newPwdAgain = request.POST['newPwdAgain']
        if len(newPwd) > 20:
            return HttpResponse('Password too long(less than20)!')
        flag = request.user.check_password(originPwd)
        if flag is False:
            status = 'Original password is not correct!'
        elif newPwd != newPwdAgain:
            status = 'New passwords are not same!'
        else:
            request.user.set_password(newPwd)
            request.user.save()
            status = 'Password changed successful!'
            auth.logout(request)
        return HttpResponse('<script>alert("密码修改成功！请重新登录");location.replace("/basicInfo/");</script>')


@login_required
def uploadPic(request):
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type == 'Student':
        item = user.student
    elif type == 'Instructor':
        item = user.instructor
    elif type == 'Manager':
        item = user.manager
    item.photo_file = request.FILES['photo']
    item.photo_file.name = str(request.user.id) + '__image.jpg'
    item.save()
    return HttpResponseRedirect('/basicInfo/changeInfo/')


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
        ret['picSrc'] = '/basicInfo/media/' + item.photo_file.name
        print(ret['picSrc'])
        ret['phoneNumber'] = item.phone_number
        ret['address'] = item.address
        ret['gender'] = '男' if (item.gender == 1) else '女'
        ret['userId'] = user.username  # Set username as ID shown outside
        if type == 'Student':
            ret['major'] = item.major.name
            ret['dept'] = item.major.department.name
        elif type == 'Instructor':
            ret['major'] = ""
            ret['dept'] = item.department.name
        else:
            ret['major'] = ''
            ret['dept'] = ''
        return render(request, 'personal_info.html', ret)
    else:
        item.address = request.POST['address']
        item.phone_number = request.POST['phoneNumber']
        item.save()
        return HttpResponse('<script> alert("修改成功！"); location.replace("/basicInfo/changeInfo/");</script>')


@login_required
def stuGradeQuery(request):
    user = request.user
    type = getType(user)
    if type != 'Student':
        return HttpResponse('You are not a student!')
    takes = Takes.objects.filter(student=user.student)
    ret = []
    for take in takes:
        if take.score is None:
            continue
        ret.append({'title': take.section.course.title, 'courseNumber': take.section.course.course_number,
                    'credit': take.section.course.credits, 'grade': take.score,
                    'gradePoint': getGradePoint(take.score)})
    return render(request, 'student/stu_grade_query.html', {'gradeList': ret, 'username': user.username})


def stuGetGPA(studentId):
    student = Student.objects.get(id=studentId)
    takes = Takes.objects.filter(student=student)
    ret = {}
    gp = 0
    totalCredits = 0
    scores = 0
    num = 0
    for take in takes:
        if take.score is None:
            continue
        scores += take.score
        num += 1
        gp += getGradePoint(take.score) * take.section.course.credits
        totalCredits += take.section.course.credits
    ret['avg'] = 0 if (num == 0) else scores * 1.0 / num
    ret['gp'] = gp
    ret['id'] = studentId
    ret['creditEarned'] = totalCredits
    ret['creditRequired'] = student.tot_cred
    if totalCredits == 0:
        ret['gpa'] = 0
    else:
        ret['gpa'] = round(gp / totalCredits, 2)
    return ret


@login_required
def stuGradeAnalysis(request):
    # TODO: 专业排名待添加
    # 学分进展功能已添加(用student.tot_cred字段)
    user = request.user
    type = getType(user)
    if type != 'Student':
        return HttpResponse('You are not a student!')
    students = Student.objects.all()
    gpa = []
    for student in students:
        gpa.append(stuGetGPA(student.id)['gpa'])
    gpa.sort()
    gpa.reverse()
    ret = stuGetGPA(user.student.id)
    ret['rank'] = gpa.index(ret['gpa']) + 1
    return render(request, 'student/stu_grade_analysis.html', ret)


@login_required
def addCourse(request):
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Instructor':
        return HttpResponse('You are not a instructor!')
    if request.method == 'GET':
        return render(request, 'instructor/instructor_course_apply.html', {'dept': user.instructor.department.name})
    else:
        course = Course()
        course.department = user.instructor.department
        course.title = request.POST['title']
        course.credits = request.POST['credits']
        course.week_hour = request.POST['weekHour']
        course.method = request.POST['method']
        course.type = request.POST['type']
        course.save()
        course.course_number = str(course.id)
        course.save()
        return HttpResponse('<script>alert("课程添加成功！");location.replace("/basicInfo/addCourse/");</script>')


@login_required
def queryCourse(request):
    ret = []
    user = User.objects.get(id=request.user.id)
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
    return render(request, 'instructor/instructor_course_query.html', {'courseList': ret})


@login_required
def gradeModify(request):
    ret = []
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Instructor':
        return HttpResponse('You are not a instructor!')
    teaches = Teaches.objects.filter(instructor=user.instructor.id)
    for teach in teaches:
        section = teach.section
        takes = Takes.objects.filter(section=section)
        if takes[0].score is None:
            continue
        course = section.course
        ret.append({
            'sectionId': teach.section.id,
            'title': course.title,
            'courseNumber': course.course_number,
            'credit': course.credits
        })
    return render(request, 'instructor/instructor_grade_modify.html', {'courseList': ret})


@login_required
def gradeInput(request):
    ret = []
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Instructor':
        return HttpResponse('You are not a instructor!')
    teaches = Teaches.objects.filter(instructor=user.instructor.id)
    for teach in teaches:
        section = teach.section
        takes = Takes.objects.filter(section=section)
        if takes.__len__() == 0 or takes[0].score is not None:
            continue
        course = section.course
        ret.append({
            'sectionId': teach.section.id,
            'title': course.title,
            'courseNumber': course.course_number,
            'credit': course.credits
        })
    return render(request, 'instructor/instructor_grade_input.html', {'courseList': ret})


@login_required
def gradeInputDetails(request):
    ret = []
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Instructor':
        return HttpResponse('You are not a instructor!')
    if request.method == 'GET':
        takes = Takes.objects.filter(section=Section.objects.get(id=request.GET['sectionId']))
        flag = 0
        for take in takes:
            grade = take.score
            if grade is None:
                flag = 1
            ret.append({
                'username': take.student.user.get_username(),
                'grade': '' if (take.score is None) else take.score
            })
        if flag == 1:
            return render(request, 'instructor/instructor_grade_input_details.html',
                          {'gradeList': ret, 'sectionId': request.GET['sectionId'],
                           'courseNumber': request.GET['courseNumber']})
        else:
            return render(request, 'instructor/instructor_grade_modify_details.html',
                          {'gradeList': ret, 'sectionId': request.GET['sectionId'],
                           'courseNumber': request.GET['courseNumber']})
    else:
        section = Section.objects.get(id=request.POST['sectionId'])
        takes = Takes.objects.filter(section=section)
        for take in takes:
            username = take.student.user.get_username()
            take.score = request.POST[username]
            take.save()
        return HttpResponse('<script>alert("成绩输入成功！");</script>')


@login_required
def gradeQuery(request):
    ret = []
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Instructor':
        return HttpResponse('You are not a instructor!')
    teaches = Teaches.objects.filter(instructor=user.instructor)
    for teach in teaches:
        section = teach.section
        takes = Takes.objects.filter(section=section)
        if takes.__len__() > 0 and takes[0].score is not None:
            ret.append({
                'sectionId': section.id,
                'courseNumber': section.course.course_number,
                'title': section.course.title,
                'credit': section.course.credits
            })
    return render(request, 'instructor/instructor_grade_query.html', {'courseList': ret})


@login_required
def gradeQueryDetails(request):
    ret = {}
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Instructor':
        return HttpResponse('You are not a instructor!')
    section = Section.objects.get(id=request.GET['sectionId'])
    takes = Takes.objects.filter(section=section)
    dis1 = 0
    dis2 = 0
    dis3 = 0
    dis4 = 0
    dis5 = 0
    gradeList = []
    total = 0
    for take in takes:
        username = str(take.student.user.get_username())
        grade = take.score
        total += grade
        gradeList.append({
            'username': username,
            'grade': grade
        })
        if grade < 60:
            dis1 += 1
        elif grade < 70:
            dis2 += 1
        elif grade < 80:
            dis3 += 1
        elif grade < 90:
            dis4 += 1
        else:
            dis5 += 1
    ret['avg'] = total / len(takes)
    ret['gradeList'] = gradeList
    ret['courseNumber'] = request.GET['courseNumber']
    ret['distribution'] = [dis1, dis2, dis3, dis4, dis5]
    return render(request, 'instructor/instructor_grade_query_details.html', ret)


@login_required
def changeCourse(request):
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Manager':
        return HttpResponse('You are not a manager!')
    if request.method == 'GET':
        try:
            course = Course.objects.get(course_number=request.GET['courseId'])
        except (UnboundLocalError, MultiValueDictKeyError):
            return render(request, 'manager/manager_course_modify.html')
        else:
            ret = {
                'courseNumber': course.course_number,
                'title': course.title,
                'credits': course.credits,
                'department': course.department.name,
                'weekHour': course.week_hour,
                'method': course.method
            }
            return JsonResponse(ret)
    else:
        courseNumber = request.POST['courseId']
        course = Course.objects.get(course_number=courseNumber)
        course.title = request.POST['title']
        course.credits = request.POST['credits']
        course.method = request.POST['method']
        course.department = Department.objects.get(name=request.POST['department'])
        course.week_hour = request.POST['weekHour']
        course.save()
        return HttpResponse('<script>alert("课程修改成功！");location.replace("/basicInfo/changeCourse/");</script>')


@login_required
def dropCourse(request):
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Manager':
        return HttpResponse('You are not a manager!')
    if request.method == 'GET':
        try:
            course = Course.objects.get(course_number=request.GET['courseId'])
        except (UnboundLocalError, MultiValueDictKeyError):
            return render(request, 'manager/manager_course_delete.html')
        else:
            ret = [{
                'courseNumber': course.course_number,
                'title': course.title,
                'credits': course.credits,
                'department': course.department.name,
                'weekHour': course.week_hour,
                'method': course.method
            }]
            return JsonResponse({'courseList': ret})
    else:
        courseIds = request.POST.getlist('courseList[]')
        for courseId in courseIds:
            course = Course.objects.get(course_number=courseId)
            course.delete()
        return HttpResponse('课程删除成功')


@login_required
def addUser(request):
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Manager':
        return HttpResponse('You are not a manager!')
    if request.method == 'GET':
        return render(request, 'manager/manager_user_add.html')
    else:
        f = request.FILES['file']
        a = f.readline().decode('gbk')
        c = 1
        while a != '':
            a.strip('\n')
            a.strip('\n')
            if a[0] == 'S':
                addType, account, name, gender, departmentName, majorName, year = a.split(' ')
                year = int(year)
            elif a[0] == 'T':
                addType, account, name, gender, departmentName = a.split(' ')
            else:
                return HttpResponse('Type error!')
            if gender != '男' and gender != '女':
                return HttpResponse('Gender is wrong!')
            if len(account) > 10:
                return HttpResponse('The account is too long!')
            user = User.objects.create_user(account, account + '@zju.edu.cn', '12345678')
            user.last_name = name
            user.save()
            department = Department.objects.filter(name=departmentName)
            if len(department) == 0:
                department = Department.objects.create(name=departmentName, building=None)
            else:
                department = department[0]
            if addType == 'S':
                student = Student()
                student.user = user
                major = Major.objects.filter(name=majorName, department=department)
                if len(major) == 0:
                    major = Major.objects.create(name=majorName, department=department)
                else:
                    major = major[0]
                student.major = major
                if gender == '男':
                    student.gender = 1
                else:
                    student.gender = 0
                student.matriculate = year
                student.save()
            else:
                instructor = Instructor()
                instructor.user = user
                if gender == '男':
                    instructor.gender = 1
                else:
                    instructor.gender = 0
                instructor.department = department
                instructor.save()
            a = f.readline().decode('gbk')
        return HttpResponse("Success")


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
def modifyUser(request):
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Manager':
        return HttpResponse('You are not a manager!')
    if request.method == 'GET':
        try:
            user = User.objects.get(username=request.GET['id'])
        except (UnboundLocalError, MultiValueDictKeyError):
            return render(request, 'manager/manager_user_query_modify.html')
        else:

            usertype = request.GET['type']
            if usertype == 'Student':
                item = user.student
            else:
                item = user.instructor
            ret = {
                'type': usertype,
                'id': user.username,
                'name': user.get_full_name(),
                'gender': '男' if (item.gender == 1) else '女',
                'address': item.address,
                'phoneNumber': item.phone_number
            }
            if usertype == 'Student':
                ret['department'] = item.major.department.name
                ret['major'] = item.major.name
            else:
                ret['department'] = item.department.name
                ret['major'] = ''
            return JsonResponse(ret)
            # return render(request, 'manager/manager_user_query_modify.html', ret)
    else:
        user = User.objects.get(username=request.POST['id'])
        usertype = request.POST['type']
        if usertype == 'Student':
            item = user.student
            item.gender = 1 if (request.POST['gender'] == '男') else 2
            item.major = Major.objects.get(name=request.POST['major'])
            item.department = Department.objects.get(name=request.POST['department'])
            item.address = request.POST['address']
            item.phone_number = request.POST['phoneNumber']
            item.save()
        else:
            item = user.instructor
            item.gender = 1 if (request.POST['gender'] == '男') else 2
            item.address = request.POST['address']
            item.department = request.POST['department']
            item.phone_number = request.POST['phoneNumber']
            item.save()
        return HttpResponse('<script>alert("信息修改成功！");location.replace("/basicInfo/modifyUser/);</script>')


@login_required
def deleteUser(request):
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Manager':
        return HttpResponse('You are not a manager!')
    if request.method == 'GET':
        try:
            user = User.objects.get(username=request.GET['username'])
        except (UnboundLocalError, MultiValueDictKeyError):
            return render(request, 'manager/manager_user_delete.html')
        else:
            usertype = request.GET['type']
            if usertype == 'Student':
                ret = {
                    'id': user.get_username(),
                    'name': user.get_full_name(),
                    'department': user.student.major.department.name
                }
            else:
                ret = {
                    'id': user.get_username(),
                    'name': user.get_full_name(),
                    'department': user.instructor.department.name
                }
            return JsonResponse(ret)
            # return render(request, 'manager/manager_user_delete.html', ret)
    else:
        usernames = request.POST.getlist('userList[]')
        for username in usernames:
            user = User.objects.get(username=username)
            user.delete()
        return HttpResponse('用户删除成功！')


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
