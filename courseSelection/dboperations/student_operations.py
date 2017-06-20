 # -*- coding: utf-8 -*- 

import datetime

from basicInfo.models import Takes, Student, Course, TimeSlot, Classroom
from courseArrange.models import Teaches, Section, SecTimeClassroom
from courseSelection.models import MajorCourse, Curriculum, CurriculumDemand, \
Selection, SelectionTime, Constants

from courseSelection.constants import *


class StudentOperations(object):

	def __init__(self, student_id):
		self.student_id = student_id
		self.student = Student.objects.get(id=self.student_id)

	def get_student_info(self):

		student_info = {}

		student_info['photo_file'] = self.student.photo_file
		student_info['phone_number'] = self.student.phone_number
		student_info['address'] = self.student.address
		student_info['tot_cred'] = self.student.tot_cred
		student_info['major'] = self.student.major.name
		student_info['matriculate'] = self.student.matriculate
		student_info['id'] = self.student_id

		user = self.student.user

		student_info['first_name'] = user.first_name
		student_info['last_name'] = user.last_name
		student_info['name'] = student_info['last_name'] + " " + student_info['first_name']

		return student_info



	def course_detail(self, course_id):
		
		course_info = {}

		course = Course.objects.get(id=course_id)

		course_info['id'] = course.id
		course_info['course_number'] = course.course_number
		course_info['title'] = course.title
		course_info['credits'] = course.credits
		course_info['week_hour'] = course.week_hour
		course_info['type'] = course.type
		course_info['method'] = course.method
		course_info['department_name'] = course.department.name

		course_info['precourse'] = []

		return course_info



	def course_select_list(self, course_id):
		return Section.objects.filter(course_id=course_id)



	def section_detail(self, section_id):
		section = Section.objects.get(id=section_id)
		section_info = {}
		try:
			section_info['semester'] = SEMESTER_DIC[section.semester]
		except:
			section_info['semester'] = section.semester
		section_info['year'] = section.year
		section_info['course_number'] = section.course.course_number
		section_info['title'] = section.course.title
		section_info['capita'] = section.max_number

		sectimeclassrooms = SecTimeClassroom.objects.filter(section_id=section_id)
		section_info['timeloc'] = []
		section_info['time'] = ""
		section_info['loc'] = ""
		for sectimeclassroom in sectimeclassrooms:
			timeloc = {}
			timeloc['time'] = self.convert_timeslot(sectimeclassroom.time_slot_id)
			section_info['time'] += timeloc['time'] + " "
			timeloc['loc'] = self.convert_classroom(sectimeclassroom.classroom_id)
			section_info['loc'] += timeloc['loc'] + " "
			section_info['timeloc'].append(timeloc)

		teaches = Teaches.objects.filter(section_id=section_id)
		section_info['instructor'] = []
		section_info['instructors'] = ""
		for teach in teaches:
			user = teach.instructor.user
			section_info['instructor'].append(user.last_name + " " + user.first_name)
			section_info['instructors'] += user.last_name + " " + user.first_name + " "

		return section_info



	def convert_timeslot(self, timeslot_id):
		timeslot = TimeSlot.objects.get(id=timeslot_id)
		time = WEEK_DAY_DIC[timeslot.day] + '第' + str(timeslot.start_time)
		for i in range(timeslot.start_time + 1, timeslot.end_time + 1):
			time += ','
			time += str(i)
		time += '节'
		return time



	def convert_classroom(self, classroom_id):
		classroom = Classroom.objects.get(id=classroom_id)
		classroomname = classroom.building + '-' + str(classroom.room_number)
		return classroomname



	def major_compulsory_course(self):
		courses = MajorCourse.objects.filter(major=self.student.major,compulsory=1)
		compulsorys = []
		credits = 0
		for course in courses:
			compulsory = {}
			compulsory['id'] = course.course.id
			compulsory['course_number'] = course.course.course_number
			compulsory['title'] = course.course.title
			compulsory['credits'] = course.course.credits
			credits += compulsory['credits']
			compulsorys.append(compulsory)
		return compulsorys, credits


	def major_elective_course(self):
		courses = MajorCourse.objects.filter(major=self.student.major,compulsory=0)
		electives = []
		for course in courses:
			elective = {}
			elective['id'] = course.course.id
			elective['course_number'] = course.course.course_number
			elective['title'] = course.course.title
			elective['credits'] = course.course.credits
			electives.append(elective)
		return electives


	def public_course(self):
		courses = Course.objects.filter(type='public')
		publics = []
		for course in courses:
			public = {}
			public['id'] = course.id
			public['course_number'] = course.course_number
			public['title'] = course.title
			public['credits'] = course.credits
			publics.append(public)
		return publics


	def curriculum_demand(self):
		major = self.student.major
		demand = CurriculumDemand.objects.get(major=major)
		elective = demand.elective
		public = demand.public
		return {'elective':elective, 'public':public}


	def formulate_curriculum(self, curriculums):

		'''
		formulate_curriculum = {'elective':[course_info_list],
		'public':[course_info_list]}
		'''

		curriculum_formulation = {}
		curriculum_formulation['elective'] = []
		curriculum_formulation['public'] = []

		for elective_id in curriculums['elective']:
			curriculum_formulation['elective'].append(section_detail[elective_id])

		for public_id in curriculums['public']:
			curriculum_formulation['public'].append(section_detail[public_id])

		# check curriculum demand
		major = self.student.major
		curriculum_demand = CurriculumDemand.objects.get(major=major)

		elective_demand = curriculum_demand.elective
		public_demand = curriculum_demand.public

		elective_credits = 0
		public_credits = 0

		for elective_course in curriculum_formulation['elective']:
			elective_credits += elective_course['credits']

		if elective_credits < elective_demand:
			raise Exception("Insufficient elective course!")

		for public_course in curriculum_formulation['public']:
			public_credits += public_course['credits']

		if public_credits < public_demand:
			raise Exception("Insufficient public course!")

		# insert
		for elective_course in curriculum_formulation['elective']:
			curriculum = Curriculum(student_id=self.student_id, course=elective_course['id'])
			curriculum.save()

		for public_course in curriculum_formulation['public']:
			curriculum = Curriculum(student_id=self.student_id, course=public_course['id'])
			curriculum.save()



	def curriculum_course(self):
		courses = Curriculum.objects.filter(student_id=self.student_id)
		curriculums = []
		credits = 0
		for course in courses:
			curriculum = {}
			curriculum['course_number'] = course.course.course_number
			curriculum['title'] = course.course.title
			curriculum['credits'] = course.course.credits
			curriculums.append(curriculum)
			credits += curriculum['credits']
		return curriculums, credits


	def check_curriculum(self):
		curriculum = Curriculum.objects.filter(student_id=self.student_id)
		if len(curriculum) == 0:
			return 0
		else:
			return 1


	def select_course(self, section_id, round, priority):

		section = Section.objects.get(id=section_id)

		# check selection time
		selection_times = self.get_selection_time()
		check_number = min(3, len(selection_times))
		intime = False

		for i in range(0, check_number):
			selection_time = selection_times[i]
			start = selection_time.start_time
			end = selection_time.end_time
			if self.check_time(start, end):
				intime = True
				break

		if not intime:
			raise Exception("Not Course Selection Time!")

		# check curriculum
		curriculum = Curriculum.objects.filter(student_id=self.student_id)

		if len(curriculum) == 0:
			raise Exception("Please Formulate Curriculum First!")

		# check capita
		selected_num = len(Selection.objects.filter(section_id=section_id)) \
		- len(Selection.objects.filter(section_id=section_id,condition=SIFTED))\
		- len(Selection.objects.filter(section_id=section_id,condition=DROPPED))
		if selected_num >= section.max_number:
			raise Exception("Exceed Course Capacity!")

		# check selection limit
		selection_limit = Constants.objects.get(name="selection_limit")
		selected_credits = self.get_selection_credits(self.student_id, semester, year)

		if selected_credits > selection_limit:
			raise Exception("Exceed the Credit Limitation!")

		# check time conflicts
		section_times = []
		sectimeclassrooms = SecTimeClassroom.objects.filter(section_id=section_id)
		for sectimeclassroom in sectimeclassrooms:
			section_times.append(sectimeclassroom.time_slot)

		selections = Selection.objects.filter(student_id=self.student_id)
		for selection in selections:
			selection_section = selection.section
			if section.term in selection_section.term:
				selected_sectimeclassrooms = SecTimeClassroom.filter(section=selection_section)
				for selected_sectimeclassroom in selected_sectimeclassrooms:
					selected_timeslot = selected_sectimeclassroom.timeslot
					for section_time in section_times:
						if selected_timeslot.day == section_time.day:
							overlapped = list(set(range(selected_timeslot.start_time, \
								selected_timeslot.end_time + 1)).intersection(set(\
								range(section_time.start_time, section_time.end_time + 1))))
							if len(overlapped) > 0:
								raise Exception("Time Conflicts!")

		# check if selected
		selected = Selection.objects.get(section_id=section_id, student_id=self.student_id)
		if selected.condition == SELECTED or selected.condition == SIFTED \
		or selected.condition == ELECTED:
			raise Exception("Course Selected!")

		if selected.condition == DROPPED: # update
			selected.condition = SELECTED
			selected.save()
			return

		# insert
		new_selection = Selection(selection_round=round,\
			select_time=datetime.datetime.now(),\
			priority=priority,\
			condition=SELECTED,\
			section_id=section_id,\
			student_id=self.student_id)
		new_selection.save()



	def get_selection_time(self):
		return SelectionTime.objects.order_by("-id")



	def check_time(self, start, end):
		now = datetime.datetime.now()
		start = start.replace(tzinfo=None)
		end = end.replace(tzinfo=None)
		if now >= start and now <= end:
			return True
		else:
			return False



	def get_selection_credits(self, semester, year):

		selected_courses = Selection.objects.filter(student_id=self.student_id)

		selected_credits = 0

		for selected_course in selected_courses:
			if selected_course.condition == ELECTED or selected_course.condition == SELECTED:
				section = selected_course.section
				if section.semester in semester and section.year == year:
					selected_credits += section.course.credits

		return selected_credits



	def drop_course(self, section_id, round):

		selected_courses = Selection.objects.filter(section_id=section_id, student_id=self.student_id)

		# check selected or not
		if len(selected) == 0:
			raise Exception("Course not Selected!")

		selected = selected_courses[0]

		if selected.condition == DROPPED:
			raise Exception("Course Dropped!")

		if selected.condition == SIFTED:
			raise Exception("Course Sifted!")

		if selected.condition == SELECTED:
			selected.delete()

		if selected.condition == ELECTED:
			# check drop number
			dropped_num = self.check_drop_number(self.student_id, semester, year)
			drop_limit = Constants.objects.get(name="drop_limit").value
			if dropped_num + 1 > drop_limit:
				raise Exception("Exceed Drop Limit!")
			# drop
			selected.condition = DROPPED
			selected.drop_time = datetime.datetime.now()
			selected.save()



	def check_drop_number(self, semester, year):

		selections = Selection.objects.filter(student_id=self.student_id,condition=DROPPED)

		dropped_num = 0

		for selection in selections:
			section = selection.Section
			if section.semester in semester and section.year == year:
				dropped_num += 1

		return dropped_num



	def search_course(self, semester, year, metric, value):

		if metric not in ['course_title', 'course_number', 'instructor', \
		'department', 'classroom', 'time']:
			raise Exception("Unvalid Metric!")

		sections = Section.objects.filter(semester=semester,year=year)

		results = []

		if metric == 'course_title':
			for section in sections:
				if value in section.course.title:
					results.append(section)
			
		elif metric == 'course_number':
			for section in sections:
				if value in section.course.course_number:
					results.append(section)

		elif metric == 'instructor':
			for section in sections:
				teaches = Teaches.objects.filter(section=section)
				for teach in teaches:
					instructor_name = teach.instructor.user.last_name + teach.instructor.user.first_name
					if value in instructor_name:
						results.append(section)

		elif metric == 'department':
			for section in sections:
				if value in section.course.department.name:
					results.append(section)

		elif metric == 'classroom':
			for section in sections:
				sectimeclassrooms = SecTimeClassroom.objects.filter(section=section)
				for sectimeclassroom in sectimeclassrooms:
					classroomname = self.convert_classroom(sectimeclassroom.classroom_id)
					if value in classroomname:
						results.append(section)

		elif metric == 'time':
			for section in sections:
				sectimeclassrooms = SecTimeClassroom.objects.filter(section=section)
				for sectimeclassroom in sectimeclassrooms:
					time_slot_id = sectimeclassroom.time_slot_id
					time = self.convert_timeslot(time_slot_id)
					if value in time:
						results.append(section)

		return results


	def schedule(self, semester, year):
		takes = Takes.objects.filter(student_id=self.student_id)
		schedules = []
		for take in takes:
			section = take.section
			if section.semester in semester and section.year == year:
				section_details = self.section_detail(section.id)
				schedules.append(section_details)
		return schedules

	def schedule_years(self):
		takes = Takes.objects.filter(student_id=self.student_id)
		years_tmp = []
		years = []
		for take in takes:
			year = take.section.year
			if year not in years_tmp:
				years_tmp.append(year)
				years.append(str(year) + '-' + str(year + 1))
		return years



