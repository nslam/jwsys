 # -*- coding: utf-8 -*- 

from django.contrib.auth.models import User
from basicInfo.models import Instructor, Student, Course, TimeSlot, Takes, Classroom, Major
from courseArrange.models import Teaches, Section, SecTimeClassroom

from courseSelection.constants import *

class InstructorOperations(object):

	def __init__(self, instructor_id):
		self.instructor_id = instructor_id
		self.instructor = Instructor.objects.get(id=self.instructor_id)

	def get_instructor_info(self):

		instructor_info = {}

		instructor_info['photo_file'] = self.instructor.photo_file
		instructor_info['phone_number'] = self.instructor.phone_number
		instructor_info['address'] = self.instructor.address
		try:
			instructor_info['department'] = self.instructor.department.name
		except:
			instructor_info['department'] = "无"

		user = self.instructor.user

		instructor_info['first_name'] = user.first_name
		instructor_info['last_name'] = user.last_name
		instructor_info['name'] = instructor_info['last_name'] + " " + instructor_info['first_name']

		return instructor_info


	def get_section_list(self):
		
		section_list = []

		teach_all = Teaches.objects.filter(instructor=self.instructor_id)

		for teach in teach_all:

			section = Section.objects.get(id=teach.section_id)

			# get section info
			section_info = {}

			section_info['section_id'] = section.id
			section_info['course'] = section.course
			try:
				section_info['semester'] = SEMESTER_DIC[section.semester]
			except:
				section_info['semester'] = section.semester
			section_info['year'] = str(section.year) + '-' + str(section.year + 1)
			section_info['max_number'] = section.max_number

			# get course info
			course = section_info['course']

			section_info['course_number'] = course.course_number
			section_info['title'] = course.title
			section_info['credits'] = course.credits
			section_info['week_hour'] = course.week_hour
			section_info['department'] = course.department

			# get time & location (array)
			section_info['time_loc'] = []

			time_loc_all = SecTimeClassroom.objects.filter(section_id=section_info['section_id'])

			for time_loc in time_loc_all:

				time_loc_info = {}

				# get time slot
				time_slot_info = {}

				time_slot = time_loc.time_slot

				time_slot_info['id'] = time_loc.id
				try:
					time_slot_info['day'] = WEEK_DAY_DIC[time_slot.day]
				except:
					time_slot_info['day'] = time_slot.day
				time_slot_info['start_time'] = time_slot.start_time
				time_slot_info['end_time'] = time_slot.end_time

				time_loc_info['time_slot'] = time_slot_info

				# get classroom
				classroom_info = {}

				classroom = time_loc.classroom

				classroom_info['id'] = classroom.id
				classroom_info['building'] = classroom.building
				classroom_info['room_number'] = classroom.room_number

				time_loc_info['classroom'] = classroom_info

				section_info['time_loc'].append(time_loc_info)

			section_list.append(section_info)

		return section_list	


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
			try:
				course_info['precourse'] = ''
				for course in course.precourse:
					course_info['precourse'] += course.title 
			except:
				course_info['precourse'] = course.precourse.title
		except:
			pass


		return course_info


	def get_student_list(self, section_id):
		
		student_list = []

		takes = Takes.objects.filter(section=section_id)

		for take in takes:

			student_info = {}

			student = take.student

			student_info['student_id'] = student.id
			student_info['phone_number'] = student.phone_number
			student_info['major'] = student.major.name

			user = student.user

			# student_info['user_id'] = user.id
			student_info['first_name'] = user.first_name
			student_info['last_name'] = user.last_name
			student_info['name'] = user.first_name + " " + user.last_name

			student_list.append(student_info)

		return student_list



