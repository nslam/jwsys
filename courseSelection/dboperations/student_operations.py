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
		course_info['type'] = COURSE_TYPE_DIC[course.type]
		course_info['method'] = course.method
		try:
			course_info['department_name'] = course.department.name
		except:
			pass

		try:
			course_info['precourse'] = ''
			for course in course.precourse:
				course_info['precourse'] += course.title 
		except:
			course_info['precourse'] = course.precourse.title

		return course_info



	def course_select_list(self, section_id):
		n_section = Section.objects.get(id=section_id)
		sections = Section.objects.filter(course_id=n_section.course_id)
		sections_info = []
		for section in sections:
			section_info = self.section_detail(section.id)
			sections_info.append(section_info)
		return sections_info



	def section_detail(self, section_id):
		section = Section.objects.get(id=section_id)
		section_info = {}
		try:
			section_info['semester'] = SEMESTER_DIC[section.semester]
		except:
			section_info['semester'] = section.semester
		section_info['year'] = section.year
		section_info['course_id'] = section.course.id
		section_info['course_number'] = section.course.course_number
		section_info['title'] = section.course.title
		section_info['capita'] = section.max_number
		section_info['section_id'] = section.id

		selections = Selection.objects.filter(section_id=section_id)
		rest_capita = section_info['capita']
		undecided_capita = 0
		for selection in selections:
			if selection.selection_condition == ELECTED:
				rest_capita -= 1
			if selection.selection_condition == SELECTED:
				undecided_capita += 1
		section_info['rest_capita'] = rest_capita
		section_info['undecided_capita'] = undecided_capita

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
		demand = CurriculumDemand.objects.filter(major=major)[0]
		elective = float(demand.elective)
		public = float(demand.public)
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
			(curriculum_formulation['elective']).append(self.course_detail(int(elective_id)))

		for public_id in curriculums['public']:
			(curriculum_formulation['public']).append(self.course_detail(int(public_id)))

		# check curriculum demand
		major = self.student.major
		curriculum_demand = CurriculumDemand.objects.filter(major=major)[0]

		elective_demand = curriculum_demand.elective
		public_demand = curriculum_demand.public

		elective_credits = 0
		public_credits = 0

		for elective_course in curriculum_formulation['elective']:
			elective_credits += elective_course['credits']

		if elective_credits < elective_demand:
			raise Exception("选修课学分不足!")

		for public_course in curriculum_formulation['public']:
			public_credits += public_course['credits']

		if public_credits < public_demand:
			raise Exception("公共课学分不足！")

		# insert
		for elective_course in curriculum_formulation['elective']:
			curriculum = Curriculum(student_id=self.student_id, course_id=elective_course['id'])
			curriculum.save()

		for public_course in curriculum_formulation['public']:
			curriculum = Curriculum(student_id=self.student_id, course_id=public_course['id'])
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



	def curriculum_sections(self):
		semester, year, selection_round = self.current_info()
		curriculums = Curriculum.objects.filter(student_id=self.student_id)
		sections = []
		for curriculum in curriculums:
			curriculum_sections = Section.objects.filter(course_id=curriculum.course_id)
			for curriculum_section in curriculum_sections:
				section = self.section_detail(curriculum_section.id)
				sections.append(section)
		return sections


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


	def current_info(self):
		selection_times = self.get_selection_time()
		check_number = min(3, len(selection_times))
		intime = False

		for i in range(0, check_number):
			selection_time = selection_times[i]
			start = selection_time.start_time
			end = selection_time.end_time
			if self.check_time(start, end):
				intime = True
				# print(selection_time.semester + str(selection_time.year) + str(selection_time.selection_round))
				return selection_time.semester, selection_time.year, selection_time.selection_round

		if not intime:
			raise Exception("非选课时间！")


	def selected_sections(self):
		semester, year, selection_round = self.current_info()
		selected_sections = Selection.objects.filter(student_id=self.student_id)
		selected = []
		for selected_section in selected_sections:
			if selected_section.section.semester in semester and\
				selected_section.section.year == year:
				section = self.section_detail(selected_section.section_id)
				section['selected_condition'] = CONDITION_DIC[selected_section.selection_condition]
				selected.append(section)
		return selected


	def section_selected(self, section_id):
		sections_selected = Selection.objects.filter(student_id=self.student_id,\
			section_id=section_id)
		sections_selected_info = []
		for section_selected in sections_selected:
			section_selected_info = self.section_detail(section_selected.section_id)
			section_selected_info['priority'] = section_selected.priority
			sections_selected_info.append(section_selected_info)
		return sections_selected_info


	def check_curriculum(self):
		curriculum = Curriculum.objects.filter(student_id=self.student_id)
		if len(curriculum) == 0:
			return 0
		else:
			return 1


	def select_course(self, section_id, priority):

		semester, year, round = self.current_info()

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
			raise Exception("非选课时间！")

		# check curriculum
		curriculum = Curriculum.objects.filter(student_id=self.student_id)

		if len(curriculum) == 0:
			raise Exception("请先制定培养方案！")

		# check capita
		selected_num = len(Selection.objects.filter(section_id=section_id)) \
		- len(Selection.objects.filter(section_id=section_id,selection_condition=SIFTED))\
		- len(Selection.objects.filter(section_id=section_id,selection_condition=DROPPED))
		if selected_num >= section.max_number:
			raise Exception("无选课余量!")

		# check selection limit
		selection_limit = float(Constants.objects.get(name="selection_limit").value)
		selected_credits = self.get_selection_credits(semester, year)

		if selected_credits > selection_limit:
			raise Exception("超过选课上限！")

		# check time conflicts
		section_times = []
		sectimeclassrooms = SecTimeClassroom.objects.filter(section_id=section_id)
		for sectimeclassroom in sectimeclassrooms:
			section_times.append(sectimeclassroom.time_slot)

		selections = Selection.objects.filter(student_id=self.student_id)
		for selection in selections:
			selection_section = selection.section
			if section.semester in selection_section.semester:
				selected_sectimeclassrooms = SecTimeClassroom.objects.filter(section=selection_section)
				for selected_sectimeclassroom in selected_sectimeclassrooms:
					selected_timeslot = selected_sectimeclassroom.time_slot
					for section_time in section_times:
						if selected_timeslot.day == section_time.day:
							overlapped = list(set(range(selected_timeslot.start_time, \
								selected_timeslot.end_time + 1)).intersection(set(\
								range(section_time.start_time, section_time.end_time + 1))))
							if len(overlapped) > 0:
								raise Exception("选课时间冲突！")

		# check if selected
		try:
			selected = Selection.objects.get(section_id=section_id, student_id=self.student_id)
			if selected.selection_condition == SELECTED or selected.selection_condition == SIFTED \
			or selected.selection_condition == ELECTED:
				raise Exception("已选该课程！")

			if selected.selection_condition == DROPPED: # update
				selected.selection_condition = SELECTED
				selected.save()
				return
				
		except:
			# insert
			new_selection = Selection(selection_round=round,\
				select_time=datetime.datetime.now(),\
				priority=priority,\
				selection_condition=SELECTED,\
				section_id=section_id,\
				student_id=self.student_id)
			new_selection.save()


	def get_selection_credits(self, semester, year):

		selected_courses = Selection.objects.filter(student_id=self.student_id)

		selected_credits = 0

		for selected_course in selected_courses:
			if selected_course.selection_condition == ELECTED or \
			selected_course.selection_condition == SELECTED:
				section = selected_course.section
				if section.semester in semester and section.year == year:
					selected_credits += section.course.credits

		return selected_credits



	def drop_course(self, section_id):

		semester, year, round = self.current_info()

		selected_courses = Selection.objects.filter(section_id=section_id, student_id=self.student_id)

		# check selected or not
		if len(selected_courses) == 0:
			raise Exception("未选择该课程!")

		selected = selected_courses[0]

		if selected.selection_condition == DROPPED:
			raise Exception("课程已退!")

		if selected.selection_condition == SIFTED:
			raise Exception("课程已刷!")

		if selected.selection_condition == SELECTED:
			selected.delete()

		if selected.selection_condition == ELECTED:
			# check drop number
			dropped_num = self.check_drop_number(semester, year)
			drop_limit = Constants.objects.get(name="drop_limit").value
			if dropped_num + 1 > drop_limit:
				raise Exception("超过退课限制!")
			# drop
			selected.selection_condition = DROPPED
			selected.drop_time = datetime.datetime.now()
			selected.save()



	def check_drop_number(self, semester, year):

		selections = Selection.objects.filter(student_id=self.student_id,\
			selection_condition=DROPPED)

		dropped_num = 0

		for selection in selections:
			section = selection.Section
			if section.semester in semester and section.year == year:
				dropped_num += 1

		return dropped_num



	def search_course(self, metric, value):

		semester, year, selection_round = self.current_info()

		if metric not in ['course_title', 'course_number', 'instructor', \
		'department', 'classroom', 'time']:
			raise Exception("Unvalid Metric!")

		year_sections = Section.objects.filter(year=year)

		sections = []
		for year_section in year_sections:
			if year_section.semester in semester:
				sections.append(year_section)

		results = []

		if metric == 'course_title':
			for section in sections:
				if value in section.course.title:
					results.append(self.section_detail(section.id))
			
		elif metric == 'course_number':
			for section in sections:
				if value in section.course.course_number:
					results.append(self.section_detail(section.id))

		elif metric == 'instructor':
			for section in sections:
				teaches = Teaches.objects.filter(section_id=section.id)
				for teach in teaches:
					instructor_name = teach.instructor.user.last_name + teach.instructor.user.first_name
					if value in instructor_name:
						results.append(self.section_detail(section.id))

		elif metric == 'department':
			for section in sections:
				if value in section.course.department.name:
					results.append(self.section_detail(section.id))

		elif metric == 'classroom':
			for section in sections:
				sectimeclassrooms = SecTimeClassroom.objects.filter(section=section)
				for sectimeclassroom in sectimeclassrooms:
					classroomname = self.convert_classroom(sectimeclassroom.classroom_id)
					if value in classroomname:
						results.append(self.section_detail(section.id))

		elif metric == 'time':
			for section in sections:
				sectimeclassrooms = SecTimeClassroom.objects.filter(section=section)
				for sectimeclassroom in sectimeclassrooms:
					time_slot_id = sectimeclassroom.time_slot_id
					time = self.convert_timeslot(time_slot_id)
					if value in time:
						results.append(self.section_detail(section.id))

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



