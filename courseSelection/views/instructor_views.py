 # -*- coding: utf-8 -*- 

from django.shortcuts import render

from courseSelection.dboperations.instructor_operations import InstructorOperations


# init
instructor_id = 1
instructorOperations = InstructorOperations(instructor_id)

def index(request):
	instructor_info = instructorOperations.get_instructor_info()
	return render(request, 'instructor/index.html', instructor_info)

def studentlist(request):
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
	if 'section' in request.GET:
		section_id = request.GET['section']
		ctx['selected_id'] = int(section_id)
		ctx['student_list'] = instructorOperations.get_student_list(section_id)
	return render(request, 'instructor/studentlist.html', ctx)

	