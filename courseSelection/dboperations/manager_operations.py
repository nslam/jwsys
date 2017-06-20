from django.contrib.auth.models import User
from basicInfo.models import Major, Student, Instructor, Takes, Manager
from courseArrange.models import Teaches, Section, SecTimeClassroom
from courseSelection.models import SelectionTime, CurriculumDemand, Selection, Constants, Curriculum
from courseSelection.constants import *
import random



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


	def set_selectionTime(self, startTime, endTime, Semester, year, SelectionRound):
		SelectionTime.objects.create(start_time=startTime, end_time=endTime,
			semester=Semester, year=year, selection_round=SelectionRound)


	def set_Curriculum(self, s_department, s_major, s_elective, s_public):
		get_major = Major.objects.get(name=s_major, department=s_department)
		CurriculumDemand.objects.get(major=get_major).update(elective=s_elective, public=s_public)


	def set_course(self, student_id, course_id, Semester, Teacher, Year):
		student = Student.objects.get(id=student_id)

		teacher = Instructor.objects.get(user=Teacher)

		teaches = Teaches.objects.filter(instructor=teacher)

		get_course = Course.objects.get(course_number=course_id)

		get_section = Section.objects.get(course=get_course, semester=Semester, year=Year)

		Takes.objects.create(student=student, section=section)

		
		tot_cred = Student.objects.get(id=student_id).tot_cred

		Student.objects.get(id=student_id).update(tot_cred=tot_cred+get_course.credits)

	def decide_selection(semester, year):
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
	

	def convey_to_takes(semester, year):
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
	
		