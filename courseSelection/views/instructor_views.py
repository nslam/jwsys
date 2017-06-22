 # -*- coding: utf-8 -*- 
import xlwt  
import re

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render

from courseSelection.dboperations.instructor_operations import InstructorOperations
from basicInfo.models import Instructor

# init
# instructor_id = 1
# instructorOperations = InstructorOperations(instructor_id)


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
	if type != 'Instructor':
	    return HttpResponse('You are not an Instructor!')
	instructor_id = Instructor.objects.get(user_id=user.id).id
	instructorOperations = InstructorOperations(instructor_id)
	instructor_info = instructorOperations.get_instructor_info()
	return render(request, 'instructor/index.html', instructor_info)

@login_required
def studentlist(request):
	user = request.user
	type = getType(user)
	if type != 'Instructor':
	    return HttpResponse('You are not an Instructor!')
	instructor_id = Instructor.objects.get(user_id=user.id).id
	instructorOperations = InstructorOperations(instructor_id)
	ctx = {}
	# get section list
	section_list = instructorOperations.get_section_list()
	sections = []
	for section_info in section_list:
		section = {}
		section['name'] = section_info['year'] + " " + section_info['semester'] + " " + \
			section_info['title']
		for timeloc in section_info['time_loc']:
			section['name'] += " " + timeloc['time_slot']['day']
		section['id'] = int(section_info['section_id'])
		sections.append(section)
	ctx['sections'] = sections
	# get student list
	if 'section' in request.GET and 'submit' in request.GET:
		if request.GET['submit'] == 'list':
			section_id = request.GET['section']
			ctx['selected_id'] = int(section_id)
			ctx['student_list'] = instructorOperations.get_student_list(section_id)
		elif request.GET['submit'] == 'down':
			section_id = request.GET['section']
			ctx['selected_id'] = int(section_id)
			student_list = instructorOperations.get_student_list(section_id)
			ctx['student_list'] = student_list
			wbk = xlwt.Workbook(encoding='utf-8')  
			ws = wbk.add_sheet((instructorOperations.course_detail(section_id))['title'], \
				cell_overwrite_ok=True)
			ws.write(0, 0, '学号')
			ws.write(0, 1, '姓名')
			ws.write(0, 2, '专业')
			ws.write(0, 3, '电话')
			row = 1
			for student_info in student_list:
				ws.write(row, 0, student_info['student_id'])
				ws.write(row, 1, student_info['name'])
				ws.write(row, 2, student_info['major'])
				ws.write(row, 3, student_info['phone_number'])
				row += 1
			response = HttpResponse(content_type='application/vnd.ms-excel') 
			response['Content-Disposition'] = 'attachment; filename=' + \
				(instructorOperations.course_detail(section_id))['title'] + '.xls' 
			wbk.save(response)
			return response
		else:
			return 0

	return render(request, 'instructor/studentlist.html', ctx)

	