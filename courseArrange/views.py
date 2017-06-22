from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from .models import *


# Create your views here.

def index(request):
    return render(request, 'index.html')


def pageAutoCourseArrange(request):
    return render(request, 'auto_course_arrange.html')


def pageManuCourseArrange(request):
    return render(request, 'manu_course_arrange.html')


def pageClassroomInput(request):
    return render(request, 'classroom_input.html')


def pageClassroomDelete(request):
    return render(request, 'classroom_delete.html')


def pageClassroomAlter(request):
    return render(request, 'classroom_alter.html')


def pageInstrCourseQuery(request):
    return render(request, 'instr_course_query.html')


def pageClassroomCourseQuery(request):
    return render(request, 'classroom_course_query.html')


def classroomManuInput(request):  # building, room_num, classroom_capacity, classroom_type("1" for 普通教室, "2" for 多媒体教室）
    building = request.POST.get('building')
    room_num = request.POST.get('room_num')
    classroom_capacity = int(request.POST.get('classroom_capacity'))
    classroom_type = int(request.POST.get('classroom_type'))
    if Classroom.objects.filter(building=building, room_number=room_num).exists():
        status = "教室信息已存在！"
    else:
        classroom = Classroom(building=building, room_number=room_num, capacity=classroom_capacity, type=classroom_type)
        classroom.save()
        status = "教室信息插入成功！"
    return render(request, 'classroom_input.html', {'status': status})


def classroomFileInput(request):
    upload_file = request.FILES.get('upload_file')
    i = 0
    status = ""
    for line in upload_file:
        line_str = line.decode(encoding='utf-8')
        i = i + 1
        list1 = line_str.split(' ')
        building = list1[0]
        room_num = list1[1]
        capacity = int(list1[2])
        type = int(list1[3])
        if Classroom.objects.filter(building=building, room_number=room_num).exists():
            status += "第%d条信息已存在！\n" % i
        else:
            classroom = Classroom(building=building, room_number=room_num, capacity=capacity, type=type)
            classroom.save()
    status += "导入成功！"
    return render(request, 'classroom_input.html', {'status': status})


def classroomDelete(request):  # building, room_num
    building = request.POST.get('building')
    room_num = request.POST.get('room_num')
    if Classroom.objects.filter(building=building, room_number=room_num).exists():
        Classroom.objects.filter(building=building, room_number=room_num).delete()
        status = "教室信息删除成功！"
    else:
        status = "教室不存在，请重试！"
    return render(request, 'classroom_delete.html', {'status': status})


def classroomAlter(request):  # building, room_num, classroom_capacity, classroom_type("1" for 普通教室, "2" for 多媒体教室）
    building = request.POST.get('building')
    room_num = request.POST.get('room_num')
    classroom_capacity = int(request.POST.get('classroom_capacity'))
    classroom_type = int(request.POST.get('classroom_type'))
    if Classroom.objects.filter(building=building, room_number=room_num).exists():
        classroom = Classroom.objects.filter(building=building, room_number=room_num)
        classroom.update(building=building, room_number=room_num, capacity=classroom_capacity, type=classroom_type)
        status = "教室信息更新成功！"
    else:
        status = "教室不存在，请重试！"
    return render(request, 'classroom_alter.html', {'status': status})


def manuCourseArrange(
        request):  # course_instr_id, course_id, building, room_num, course_capacity, day(1-7), start_time(1-13), end_time(1-13)
    user_name = request.POST.get('course_instr_id')
    course_num = request.POST.get('course_id')
    capacity = int(request.POST.get('course_capacity'))
    building = request.POST.get('building1')
    room_num = request.POST.get('room_num1')
    day = int(request.POST.get('day1'))
    start_time = int(request.POST.get('start_time1'))
    end_time = int(request.POST.get('end_time1'))
    flag = 0
    if not Course.objects.filter(course_number=course_num).exists():
        status = "不存在该课程！"
    elif not User.objects.filter(username=user_name).exists():
        status = "不存在该教师！"
    elif not Classroom.objects.filter(building=building, room_number=room_num):
        status = "不存在该教室！"
    elif TimeSlot.objects.filter(day=day, start_time=start_time, end_time=end_time).exists():
        time = TimeSlot.objects.get(day=day, start_time=start_time, end_time=end_time)
        classroom = Classroom.objects.get(building=building, room_number=room_num)
        if SecTimeClassroom.objects.filter(time_slot=time, classroom=classroom).exists():
            status = "时间冲突！"
        elif classroom.capacity < capacity:
            status = "教室容量不足！"
        else:
            instructor = User.objects.get(username=user_name).instructor
            course = Course.objects.get(course_number=course_num)
            list1 = Teaches.objects.filter(instructor=instructor)
            list2 = Section.objects.filter(course=course)
            for obj_1 in list1:
                for obj_2 in list2:
                    if obj_1.section == obj_2:
                        section = obj_2
                        flag = 1
            if flag == 1:
                SecTimeClassroom.objects.filter(section=section).update(classroom=classroom, time_slot=time)
                status = "手动调课成功！"
            else:
                status = "该教师未开设该门课程！"
    else:
        status = "不存在此时间段！"
    return render(request, 'manu_course_arrange.html', {'status': status})


def instrCourseQuery(request):  # instr_id
    time = ""
    room = ""
    teacher_name = ""
    ret = []
    user_name = request.POST.get('instr_id')
    if not User.objects.filter(username=user_name).exists():
        status = "不存在该教师！"
        return render(request, 'instr_course_query.html', {'status': status})
    else:
        instructor = User.objects.get(username=user_name).instructor
        p = Teaches.objects.filter(instructor=instructor)
        for obj in p:
            section = obj.section
            t = Teaches.objects.filter(section=section)
            for q in t:
                instructor = q.instructor
                name = User.objects.get(instructor=instructor).get_full_name()
                teacher_name += "%s\n" % name
            course = section.course
            semester = section.semester
            max_num = section.max_number
            course_num = course.course_number
            course_name = course.title
            stcs = SecTimeClassroom.objects.filter(section=section)
            for stc in stcs:
                time_slot = stc.time_slot
                day = time_slot.day
                start = time_slot.start_time
                end = time_slot.end_time
                time += "周%d第%d~%d节\n" % (day, start, end)
                classroom = stc.classroom
                building = classroom.building
                room_num = classroom.room_number
                room += "%s-%s" % (building, room_num)
                type = classroom.type
                if type == "1":
                    room += "\n"
                else:
                    room += "（多）\n"
            ret.append(
                {'course_num': course_num, 'course_name': course_name, 'semester': semester, 'time': time, 'room': room,
                 'teacher_name': teacher_name, 'max_num': max_num})
            teacher_name = ""
            room = ""
            time = ""
        return render(request, 'course_query_result.html', {'ret': ret})


def classroomCourseQuery(request):  # building, room_num
    ret = []
    teacher_name = ""
    time = ""
    room = ""
    building = request.POST.get('building')
    room_num = request.POST.get('room_num')
    if Classroom.objects.filter(building=building, room_number=room_num).exists():
        classroom = Classroom.objects.get(building=building, room_number=room_num)
        p = SecTimeClassroom.objects.filter(classroom=classroom).order_by('section')
        for obj in p:
            section = obj.section
            max_num = section.max_number
            semester = section.semester
            course = section.course
            course_name = course.title
            course_num = course.course_number
            ts = Teaches.objects.filter(section=section)
            for t in ts:
                teacher = t.instructor
                name = User.objects.get(instructor=teacher).get_full_name()
                teacher_name += "%s\n" % name
            stcs = SecTimeClassroom.objects.filter(section=section, classroom=classroom)
            for stc in stcs:
                timeslot = stc.time_slot
                day = timeslot.day
                start = timeslot.start_time
                end = timeslot.end_time
                classroom = stc.classroom
                building = classroom.building
                room_num = classroom.room_number
                type = classroom.type
                time += "周%d第%d~%d节\n" % (day, start, end)
                room += "%s-%s" % (building, room_num)
                if type == "1":
                    room += "\n"
                else:
                    room += "（多)\n"
            ret.append(
                {'course_num': course_num, 'course_name': course_name, 'semester': semester, 'time': time, 'room': room,
                 'teacher_name': teacher_name,
                 'max_num': max_num})  # course_id,course_name,semester,time,location,teacher_name,capacity
            teacher_name = ""
            room = ""
            time = ""
        return render(request, 'course_query_result.html', {'ret': ret})
    else:
        status = "教室不存在，请重试！"
        return render(request, 'classroom_course_query.html', {'status': status})


def instrBusyTimeSetting(request):  # instr_id, day, day(1-7), start_time(1-13), end_time(1-13)
    username = request.POST.get('instr_id')
    day = int(request.POST.get('day'))
    start_time = int(request.POST.get('start_time'))
    end_time = int(request.POST.get('end_time'))
    if start_time > end_time:
        status = "时间段输入不正确！"
    elif User.objects.filter(username=username).exists():
        instructor = User.objects.get(username=username).instructor
        new_obj = InstructorBusyTime(instructor=instructor, day=day, start_time=start_time, end_time=end_time)
        new_obj.save()
        status = "教师忙碌时间录入成功！"
    else:
        status = "不存在该教师，请重试！"
    return render(request, 'auto_course_arrange.html', {'status': status})


def courseInstrSetting(request):  # course_id, course_instr_id, course_capacity, classroom_requirement
    course_num = request.POST.get('course_id')
    username = request.POST.get('course_instr_id')
    capacity = int(request.POST.get('course_capacity'))
    classroom_req = int(request.POST.get('classroom_requirement'))
    if not Course.objects.filter(course_number=course_num).exists():
        status = "该课程不存在，请重试！"
    elif not User.objects.filter(username=username).exists():
        status = "该教师不存在，请重试！"
    elif CourseCandidate.objects.filter(instructor=User.objects.get(username=username).instructor,
                                        course=Course.objects.get(course_number=course_num)).exists():
        status = "开课信息已存在！"
    else:
        instructor = User.objects.get(username=username).instructor
        course = Course.objects.get(course_number=course_num)
        obj = CourseCandidate(instructor=instructor, course=course, capacity=capacity, classroom_type=classroom_req)
        obj.save()
        status = "教师开课成功！"
    return render(request, 'auto_course_arrange.html', {'status': status})


def autoCourseArrange(request):  # no args
    return render(request, 'index.html')

