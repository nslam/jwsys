from django.contrib.auth.models import User
from basicInfo.models import Major, Student, Instructor, Takes, Manager
from courseArrange.models import Teaches, Section, SecTimeClassroom
from courseSelection.models import SelectionTime, CurriculumDemand, Selection, Constants, Curriculum
from courseSelection.constants import *
import random
import datetime


#from courseSelection.models import Selection, Constants, Curriculum
#from courseArrange.models import Section
#from basicInfo.models import Takes

#from courseSelection.constants import *

class ManagerOperations(object):
	"""docstring for ClassName"""
	def __init__(self, manager_id):
		self.manager_id = manager_id
		self.manager = Manager.objects.get(id=manager_id)

	def get_manager_info(self):
		manager_info = {}
		manager_info['photo_file'] = self.manager.photo_file
		manager_info['phone_number'] = self.manager.phone_number
		manager_info['address'] = self.manager.address

		user_id = self.manager.user_id
		user = User.objects.get(id=user_id)

		manager_info['first_name'] = user.first_name
		manager_info['last_name'] = user.last_name

		return manager_info


	def set_selection_time(self, startTime, endTime, Semester, year, SelectionRound):
		SelectionTime.objects.create(start_time=startTime, end_time=endTime,
			semester=Semester, year=year, selection_round=SelectionRound)


	def set_curriculum(self, major_id, s_elective, s_public):
		curriculumDemand = CurriculumDemand.objects.filter(major_id=major_id)
		if len(curriculumDemand) > 0:
			curriculumDemand.elective = s_elective
			curriculumDemand.public = s_public
			curriculumDemand.save()
		else:
			curriculumDemand = CurriculumDemand(major_id=major_id, elective=s_elective, public=s_public)
			curriculumDemand.save()


	def set_course(self, student_id, course_id, Semester, Teacher, Year):
		student = Student.objects.get(id=student_id)

		teacher = Instructor.objects.get(user=Teacher)

		teaches = Teaches.objects.filter(instructor=teacher)

		get_course = Course.objects.get(course_number=course_id)

		get_section = Section.objects.get(course=get_course, semester=Semester, year=Year)

		Takes.objects.create(student=student, section=section)

		
		tot_cred = Student.objects.get(id=student_id).tot_cred

		Student.objects.get(id=student_id).update(tot_cred=tot_cred+get_course.credits)


	def decide_selection(self, semester, year):
		curriculum_percentage = Constants.objects.get(name='selection_curriculum_percentage').value
		sections = Section.objects.filter(year=year)
		undecided_sections = []
		for section in sections:

			if section.semester in semester:
				undecided_selections = Selection.objects.filter(\
					section=section,selection_condition=SELECTED)
				elected_selections = Selection.objects.filter(\
					section=section,selection_condition=ELECTED)
				capita = section.max_number - len(elected_selections)
				if capita <= 0:
					continue

				# not fully selected, all elected
				if capita >= len(undecided_selections): 
					for undecided_selection in undecided_selections:
						undecided_selection.selection_condition = ELECTED
						undecided_selection.save()
				
				else: # otherwise, fully selected, sift some
					curriculum_capita = int(capita * curriculum_percentage)

					# get curriculum privilege
					privilege_selections = []
					nonprivilege_selections = []
					for undecided_selection in undecided_selections:
						privilege_flag = 0
						curriculums = Curriculum.objects.filter(\
							student_id=undecided_selection.student_id)
						for curriculum in curriculums:
							if curriculum.course_id == undecided_selection.section.course_id:
								privilege_selections.append(undecided_selection)
								privilege_flag = 1
								break
						if privilege_flag == 0:
							nonprivilege_selections.append(undecided_selection)

					# privilege capita not full, non privilege overflow
					if len(privilege_selections) <= curriculum_capita:
						for privilege_selection in privilege_selections: # all privileged elected
							privilege_selection.selection_condition = ELECTED
							privilege_selection.save()
						# non privilege
						capita_remainder = capita - len(privilege_selections)
						first_nonprivilege_selections = []
						second_nonprivilege_selections = []
						third_nonprivilege_selections = []
						for nonprivilege_selection in nonprivilege_selections:
							if nonprivilege_selection.priority == 1:
								first_nonprivilege_selections.append(nonprivilege_selection)
							elif nonprivilege_selection.priority == 2:
								second_nonprivilege_selections.append(nonprivilege_selection)
							elif nonprivilege_selection.priority == 3:
								third_nonprivilege_selections.append(nonprivilege_selection)
							else:
								pass
						# priority 1
						if len(first_nonprivilege_selections) <= capita_remainder:
							for first_nonprivilege_selection in first_nonprivilege_selections:
								first_nonprivilege_selection.selection_condition = ELECTED
								first_nonprivilege_selection.save()
							capita_remainder = capita_remainder - len(first_nonprivilege_selections)
							# priority 2
							if len(second_nonprivilege_selections) <= capita_remainder:
								for second_nonprivilege_selection in second_nonprivilege_selections:
									second_nonprivilege_selection.selection_condition = ELECTED
									second_nonprivilege_selection.save()
								# priority 3
								capita_remainder = capita_remainder - len(second_nonprivilege_selections)
								elections = random.sample(third_nonprivilege_selections, capita_remainder)
								for election in elections:
									election.selection_condition = ELECTED
									election.save()
							else:
								elections = random.sample(second_nonprivilege_selections, capita_remainder)
								for election in elections:
									election.selection_condition = ELECTED
									election.save()
						else:
							elections = random.sample(first_nonprivilege_selections, capita_remainder)
							for election in elections:
								election.selection_condition = ELECTED
								election.save()

					else: # privilege capita full
						elections = random.sample(privilege_selections, curriculum_capita)
						for election in elections:
							election.selection_condition = ELECTED
							election.save()
						# non privilege
						capita_remainder = capita - curriculum_capita
						first_nonprivilege_selections = []
						second_nonprivilege_selections = []
						third_nonprivilege_selections = []
						for nonprivilege_selection in nonprivilege_selections:
							if nonprivilege_selection.priority == 1:
								first_nonprivilege_selections.append(nonprivilege_selection)
							elif nonprivilege_selection.priority == 2:
								second_nonprivilege_selections.append(nonprivilege_selection)
							elif nonprivilege_selection.priority == 3:
								third_nonprivilege_selections.append(nonprivilege_selection)
							else:
								pass
						# priority 1
						if len(first_nonprivilege_selections) <= capita_remainder:
							for first_nonprivilege_selection in first_nonprivilege_selections:
								first_nonprivilege_selection.selection_condition = ELECTED
								first_nonprivilege_selection.save()
							capita_remainder = capita_remainder - len(first_nonprivilege_selections)
							# priority 2
							if len(second_nonprivilege_selections) <= capita_remainder:
								for second_nonprivilege_selection in second_nonprivilege_selections:
									second_nonprivilege_selection.selection_condition = ELECTED
									second_nonprivilege_selection.save()
								# priority 3
								capita_remainder = capita_remainder - len(second_nonprivilege_selections)
								elections = random.sample(third_nonprivilege_selections, capita_remainder)
								for election in elections:
									election.selection_condition = ELECTED
									election.save()
							else:
								elections = random.sample(second_nonprivilege_selections, capita_remainder)
								for election in elections:
									election.selection_condition = ELECTED
									election.save()
						else:
							elections = random.sample(first_nonprivilege_selections, capita_remainder)
							for election in elections:
								election.selection_condition = ELECTED
								election.save()

		return SUCCESS
	

	def convey_to_takes(self, semester, year):
		elected_selections = Selection.objects.filter(selection_condition=ELECTED)
		for elected_selection in elected_selections:
			section = elected_selection.section
			if section.semester in semester and section.year == year:
				take_existence = Takes.objects.filter(section_id=elected_selection.section_id,\
					student_id=elected_selection.student_id)
				if len(take_existence) == 0:
					take = Takes(section_id=elected_selection.section_id,\
						student_id=elected_selection.student_id)
					take.save()
		return SUCCESS


	def all_majors(self):
		majors_info = []
		majors = Major.objects.all()
		for major in majors:
			major_info = {}
			major_info['id'] = major.id
			major_info['name'] = major.name
			majors_info.append(major_info)
		return majors_info


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


	def select_course(self, section_id, student_id):

		semester, year, round = self.current_info()

		section = Section.objects.get(id=section_id)

		# check if selected
		try:
			selected = Selection.objects.get(section_id=section_id, student_id=student_id)
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
				priority=0,\
				selection_condition=SELECTED,\
				section_id=section_id,\
				student_id=student_id)
			new_selection.save()


	
		