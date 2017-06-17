from courseSelection.models import Takes, Teaches, Student, Section, Course


def get_student_info(student_id):

	student_info = {}

	student = Student.objects.get(id=student_id)

	student_info['photo_file'] = student.photo_file
	student_info['phone_number'] = student.phone_number
	student_info['address'] = student.address
	student_info['tot_cred'] = student.tot_cred
	student_info['major'] = student.major
	student_info['college'] = student.college

	user_id = student.user_id
	user = User.objects.get(id=user_id)

	student_info['first_name'] = user.first_name
	student_info['last_name'] = user.last_name

	return student_info


def formulate_curriculum(student_id):
	pass


def select_course():
	pass


def check_time_conflicts():
	pass


def drop_course():
	pass


def check_drop_number():
	pass


def search_course():
	pass


def course_detail(course_id):
	
	course_info = {}

	course = Course.objects.



def show_curriculum_course():
	pass


