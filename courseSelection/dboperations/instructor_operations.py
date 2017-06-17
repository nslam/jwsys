from courseSelection.models import Teaches, User, Instructor, \
Student, Section, Course, SecTimeClassroom, TimeSlot


class InstructorOperations(object):

	def __init__(self, instructor_id):
		self.instructor_id = instructor_id

	def get_instructor_info(self, instructor_id = self.instructor_id):

		instructor_info = {}

		instructor = Instructor.objects.get(id=instructor_id)

		instructor_info['photo_file'] = instructor.photo_file
		instructor_info['phone_number'] = instructor.phone_number
		instructor_info['address'] = instructor.address

		user_id = instructor.user_id
		user = User.objects.get(id=user_id)

		instructor_info['first_name'] = user.first_name
		instructor_info['last_name'] = user.last_name

		return instructor_info


	def get_section_list(self, instructor_id = self.instructor_id):
		
		section_list = []

		teach_all = Teaches.objects.filter(instructor=instructor_id)

		for teach in teach_all:

			section = Section.objects.get(id=teach.section)

			# get section info
			section_info = {}

			section_info['section_id'] = section.id
			section_info['course_id'] = section.course
			section_info['semester'] = section.semester
			section_info['year'] = section.year
			section_info['max_number'] = section.max_number

			# get course info
			course = Course.objects.get(id=section_info['course_id'])

			section_info['course_number'] = course.course_number
			section_info['title'] = course.title
			section_info['credits'] = course.credits
			section_info['week_hour'] = course.week_hour
			section_info['department'] = course.department

			# get time & location (array)
			section_info['time_loc'] = []

			time_loc_all = SecTimeClassroom.filter(section=section_info['section_id'])

			for time_loc in time_loc_all:

				time_loc_info = {}

				# get time slot
				time_slot_info = {}

				time_slot_id = time_loc.time_slot
				time_slot = TimeSlot.filter(id=time_slot_id)

				time_slot_info['day'] = time_slot.day
				time_slot_info['start_time'] = time_slot.start_time
				time_slot_info['end_time'] = time_slot.end_time

				time_loc_info['time_slot'] = time_slot_info

				# get classroom
				classroom_info = {}

				classroom_id = time_loc.classroom
				classroom = Classroom.get(id=classroom_id)

				classroom_info['building'] = classroom.building
				classroom_info['room_number'] = classroom.room_number

				time_loc_info['classroom'] = classroom_info

				section_info['time_loc'].append(time_loc_info)

			section_list.append(section_info)

		return section_list	


	def get_student_list(self, section_id):
		
		student_list = []

		takes = Takes.objects.filter(section=section_id)

		for take in takes:

			student_info = {}

			student = Student.objects.get(id=take.student)

			student_info['student_id'] = student.id
			student_info['phone_number'] = student.phone_number
			student_info['major'] = Major.objects.get(id=student.major).name

			user_id = student.user_id
			user = User.objects.get(id=user_id)

			student_info['first_name'] = user.first_name
			student_info['last_name'] = user.last_name

			student_list.append(student_info)

		return student_list



