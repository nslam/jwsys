from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from basicInfo.models import Student

from courseSelection.dboperations.student_operations import StudentOperations
from django.contrib.auth.decorators import login_required



# init
# student_id = 1
# studentOperations = StudentOperations(student_id)


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


@login_required
def index(request):
	user = request.user
	type = getType(user)
	if type != 'Student':
	    return HttpResponse('You are not a Student!')
	student_id = Student.objects.get(user_id=user.id).id
	studentOperations = StudentOperations(student_id)

	student_info = studentOperations.get_student_info()
	return render(request, 'student/index.html', student_info)

@login_required
def curriculum(request):
	user = request.user
	type = getType(user)
	if type != 'Student':
	    return HttpResponse('You are not a Student!')
	student_id = Student.objects.get(user_id=user.id).id
	studentOperations = StudentOperations(student_id)

	ctx = {}
	ctx['demand'] = studentOperations.curriculum_demand()
	check_curriculum = studentOperations.check_curriculum()
	ctx['check_curriculum'] = check_curriculum
	ctx['compulsory'], ctx['compulsory_credits'] = studentOperations.major_compulsory_course()
	if check_curriculum == 0:
		ctx['elective'] = studentOperations.major_elective_course()
		ctx['public'] = studentOperations.public_course()
	else:
		ctx['curriculum'], ctx['credits'] = studentOperations.curriculum_course()

	if request.method == 'POST':
		selected = {}
		selected['elective'] = request.POST.getlist("elective")
		selected['public'] = request.POST.getlist("public")
		try:
			studentOperations.formulate_curriculum(selected)
			return HttpResponseRedirect("curriculum")
		except Exception as err:
			return render(request, 'student/curriculum_result.html', {'result':err})

	return render(request, 'student/curriculum.html', ctx)


@login_required
def selection(request):
	user = request.user
	type = getType(user)
	if type != 'Student':
	    return HttpResponse('You are not a Student!')
	student_id = Student.objects.get(user_id=user.id).id
	studentOperations = StudentOperations(student_id)

	ctx = {}
	try:
		ctx['sections'] = studentOperations.curriculum_sections()
		ctx['selected'] = studentOperations.selected_sections()
	except Exception as err:
		ctx['result'] = err
		return render(request, 'student/selection_condition.html', ctx)
	if 'metric' in request.GET and 'value' in request.GET:
		ctx['sections'] = studentOperations.search_course(request.GET['metric'],request.GET['value'])
	return render(request, 'student/selection.html', ctx)


@login_required
def dropcourse(request):
	user = request.user
	type = getType(user)
	if type != 'Student':
	    return HttpResponse('You are not a Student!')
	student_id = Student.objects.get(user_id=user.id).id
	studentOperations = StudentOperations(student_id)

	ctx = {}
	if request.method == "POST":
		section_id = request.POST['drop']
		try:
			studentOperations.drop_course(section_id)
			ctx['result'] = '退课成功！'
		except Exception as err:
			ctx['result'] = err
	return render(request, 'student/selection_drop.html', ctx)


@login_required
def selectionpriority(request):
	user = request.user
	type = getType(user)
	if type != 'Student':
	    return HttpResponse('You are not a Student!')
	student_id = Student.objects.get(user_id=user.id).id
	studentOperations = StudentOperations(student_id)

	ctx = {}
	if request.method == "GET":
		section_id = request.GET['select']
		try:
			ctx['sections'] = studentOperations.course_select_list(section_id)
			ctx['sections_selected'] = studentOperations.section_selected(section_id)
			return render(request, 'student/priority.html', ctx)
		except Exception as err:
			ctx['result'] = err
		return render(request, 'student/selection_drop.html', ctx)


@login_required
def selectionresult(request):
	user = request.user
	type = getType(user)
	if type != 'Student':
	    return HttpResponse('You are not a Student!')
	student_id = Student.objects.get(user_id=user.id).id
	studentOperations = StudentOperations(student_id)

	ctx = {}
	if request.method == "GET":
		section_id = request.GET['select']
		try:
			studentOperations.select_course(int(section_id),1)
			ctx['result'] = "选课成功！"
		except Exception as err:
			ctx['result'] = err
		return render(request, 'student/selection_result.html', ctx)
	else:
		ctx['result'] = '未收到请求'
		return render(request, 'student/selection_result.html', ctx)


@login_required
def coursedetails(request):
	user = request.user
	type = getType(user)
	if type != 'Student':
	    return HttpResponse('You are not a Student!')
	student_id = Student.objects.get(user_id=user.id).id
	studentOperations = StudentOperations(student_id)

	ctx = {}
	if request.method == "GET":
		if 'id' in request.GET:
			course_id = request.GET['id']
			ctx = studentOperations.course_detail(course_id)
	return render(request, 'student/coursedetails.html', ctx)


@login_required
def schedule(request):
	user = request.user
	type = getType(user)
	if type != 'Student':
	    return HttpResponse('You are not a Student!')
	student_id = Student.objects.get(user_id=user.id).id
	studentOperations = StudentOperations(student_id)

	ctx = {}
	ctx['years'] = studentOperations.schedule_years()
	if 'year' in request.GET:
		selected_year = request.GET['year']
		ctx['selected_year'] = selected_year
		if 'semester' in request.GET:
			selected_semester = request.GET['semester']
			ctx['selected_semester'] = selected_semester
			if selected_semester == 'springsummer':
				semester = 'spring&autumn'
			elif selected_semester == 'autumnwinter':
				semester = 'autumn&winter'
			else:
				pass
			schedules = studentOperations.schedule(semester, int(selected_year[0:4]))
			ctx['schedules'] = schedules
	return render(request, 'student/schedule.html', ctx)


