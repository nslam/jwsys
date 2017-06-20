from django.shortcuts import render

from courseSelection.dboperations.student_operations import StudentOperations


# init
student_id = 1
studentOperations = StudentOperations(student_id)

def index(request):
	student_info = studentOperations.get_student_info()
	return render(request, 'student/index.html', student_info)

def curriculum(request):
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
	# if request.POST.getlist("elective") != None:
	# 	selected = {}
	# 	selected['elective'] = request.POST.getlist("elective")
	# 	selected['public'] = request.POST.getlist("public")
	# 	studentOperations.formulate_curriculum(selected)
	return render(request, 'student/curriculum.html', ctx)

def selection(request):
	a = 1
	return render(request, 'student/selection.html')

def selectionpriority(request):
	a = 1
	return render(request, 'student/priority.html')

def coursedetails(request):
	a = 1
	return render(request, 'student/coursedetails.html')

def schedule(request):
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


