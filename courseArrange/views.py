from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from basicInfo.views import getType


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')

@login_required
def pageAutoCourseArrange(request):
    return render(request, 'auto_course_arrange.html')

@login_required
def pageManuCourseArrange(request):
    return render(request, 'manu_course_arrange.html')

@login_required
def pageClassroomInput(request):
    return render(request, 'classroom_input.html')

@login_required
def pageClassroomDelete(request):
    return render(request, 'classroom_delete.html')

@login_required
def pageClassroomAlter(request):
    return render(request, 'classroom_alter.html')

@login_required
def pageInstrCourseQuery(request):
    return render(request, 'instr_course_query.html')

@login_required
def pageClassroomCourseQuery(request):
    return render(request, 'classroom_course_query.html')

@login_required
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

@login_required
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

@login_required
def classroomDelete(request):  # building, room_num
    building = request.POST.get('building')
    room_num = request.POST.get('room_num')
    if Classroom.objects.filter(building=building, room_number=room_num).exists():
        Classroom.objects.filter(building=building, room_number=room_num).delete()
        status = "教室信息删除成功！"
    else:
        status = "教室不存在，请重试！"
    return render(request, 'classroom_delete.html', {'status': status})

@login_required
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

@login_required
def manuCourseArrange(request):
    user_name = request.POST.get('course_instr_id')
    course_num = request.POST.get('course_id')
    capacity = int(request.POST.get('course_capacity'))
    building = request.POST.get('building')
    room_num = request.POST.get('room_num')
    day = int(request.POST.get('day'))
    start_time = int(request.POST.get('start_time'))
    end_time = int(request.POST.get('end_time'))
    old_day = int(request.POST.get('old_day'))
    old_start_time = int(request.POST.get('old_start_time'))
    old_end_time = int(request.POST.get('old_end_time'))
    flag = 0
    if not TimeSlot.objects.filter(day=old_day, start_time=old_start_time, end_time=old_end_time).exists():
        status = "不存在此时间段！请确认原来课程的时间段！"
    elif not Course.objects.filter(course_number=course_num).exists():
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
            old_timeslot = TimeSlot.objects.get(day=old_day, start_time=old_start_time, end_time=old_end_time)
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
                if SecTimeClassroom.objects.filter(section=section, time_slot=old_timeslot).exists():
                    section.capacity = capacity
                    section.save()
                    SecTimeClassroom.objects.filter(section=section, time_slot=old_timeslot).update(classroom=classroom,
                                                                                                    time_slot=time)
                    status = "手动调课成功！"
                else:
                    status = "该教师未在该时间段开课！"
            else:
                status = "该教师未开设该门课程！"
    else:
        status = "不存在此时间段！请确认调课后的时间段！"
    return render(request, 'manu_course_arrange.html', {'status': status})

@login_required
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
                time += "周%d 第%d节 - 第%d节\n" % (day, start, end)
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

@login_required
def instrCourseQuery_instr(request):
    user = User.objects.get(id=request.user.id)
    type = getType(user)
    if type != 'Instructor':
        return HttpResponse('You are not a instructor!')
    else:
        time = ""
        room = ""
        teacher_name = ""
        ret = []
        user_name = user.username
        instructor = User.objects.get(username=user_name).instructor
        p = Teaches.objects.filter(instructor=instructor)
        for obj in p:
            section = obj.section
            t = Teaches.objects.filter(section=section)
            for q in t:
                instructor = q.instructor
                name = User.objects.get(instructor=instructor).get_full_name()
                teacher_name += "%s / " % name
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
                time += "周%d 第%d节 - 第%d节\n" % (day, start, end)
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

@login_required
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
                time += "周%d 第%d节 - 第%d节\n" % (day, start, end)
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

@login_required
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

@login_required
def courseInstrSetting(request):   #course_id, course_instr_id, course_capacity, classroom_requirement
    course_num = request.POST.get('course_id')
    username = request.POST.get('course_instr_id')
    capacity = int(request.POST.get('course_capacity'))
    classroom_req = int(request.POST.get('classroom_requirement'))
    if not Course.objects.filter(course_number=course_num).exists():
        status = "该课程不存在，请重试！"
    elif not User.objects.filter(username = username).exists():
        status = "该教师不存在，请重试！"
    elif CourseCandiate.objects.filter(instructor=User.objects.get(username=username).instructor,course=Course.objects.get(course_number=course_num)).exists():
        status = "开课信息已存在！"
    else:
        flag=0
        instructor=User.objects.get(username=username).instructor
        course=Course.objects.get(course_number=course_num)
        ts=Teaches.objects.filter(instructor=instructor)
        cs=Course.objects.filter(course=course)
        for t in ts:
            for c in cs:
                if t.section==c.section:
                    flag=1
        if flag==1:
            status="该教师已开该门课程！"
        else:
            obj=CourseCandiate(instructor=instructor,course=course,capacity=capacity, classroom_type = classroom_req)
            obj.save()
            status = "教师开课成功！"
    return render(request, 'auto_course_arrange.html', {'status': status})

@login_required
def autoCourseArrange(request):  # no args
    ret = []
    unarranged = []

    class Classrooms:
        'Classrooms imf'

        def __init__(self, classroomID, capacity, type_equipment):
            self.classroomID = classroomID  # 实际存了classroom类
            self.capacity = capacity
            self.type_equipment = type_equipment
            self.timeSlot = [n for n in range(0, 25)]

    class Sections:
        'Section imf'

        def __init__(self, courseID, capacity, credits, type, teacher):
            self.courseID = courseID  # 实际存了course类
            self.capacity = capacity
            self.credits = credits
            self.type = type
            self.classroomID = 0
            self.timeSlot = []  # (0 1 2 3 4) * 5
            self.busytime = []
            self.fuck_section = 0
            self.teachername = teacher

    '''读数据'''
    ClassroomList = []
    SectionList = []
    classroomtable = Classroom.objects.all()
    for line in classroomtable:
        ClassroomList.append(Classrooms(line, line.capacity, line.type))
    sectiontable = CourseCandiate.objects.all()

    for line in sectiontable:
        teacher = User.objects.get(instructor=line.instructor).get_full_name()
        SectionList.append(Sections(line.course, \
                                    line.capacity, line.course.week_hour, line.classroom_type, \
                                    teacher))

        _621_section = Section.objects.filter(course=line.course, semester='秋冬', year=2017, max_number=line.capacity)
        if len(_621_section) == 0:
            _621_bala = Section(course=line.course, semester='秋冬', year=2017, max_number=line.capacity)
            _621_bala.save()
        SectionList[-1].fuck_section = Section.objects.get(course=line.course, max_number=line.capacity)

        _621_teacher = Teaches.objects.filter(instructor=line.instructor, section=SectionList[-1].fuck_section)
        if len(_621_teacher) == 0:
            _621_balabala = Teaches(instructor=line.instructor, section=SectionList[-1].fuck_section)
            _621_balabala.save()

        if InstructorBusyTime.objects.filter(instructor=line.instructor).exists():
            temp_fuck = InstructorBusyTime.objects.filter(instructor=line.instructor)
            i = temp_fuck.start_time
            while i <= temp_fuck.end_time:
                if i in [1, 2, 3]:
                    SectionList[-1].busytime.append(0 + (temp_fuck.day - 1) * 5)
                    i = 4
                elif i in [4, 5]:
                    SectionList[-1].busytime.append(1 + (temp_fuck.day - 1) * 5)
                    i = 6
                elif i in [6, 7, 8]:
                    SectionList[-1].busytime.append(2 + (temp_fuck.day - 1) * 5)
                    i = 9
                elif i in [9, 10]:
                    SectionList[-1].busytime.append(3 + (temp_fuck.day - 1) * 5)
                    i = 11
                elif i in [11, 12, 13]:
                    SectionList[-1].busytime.append(4 + (temp_fuck.day - 1) * 5)
                    i = 14
                else:
                    break

    def sortSection(x):
        return x.capacity

    SectionList.sort(key=sortSection, reverse=True)

    def findSuitTime(x):
        temp = x % 5
        if temp == 2 or temp == 0:
            return x
        elif temp == 4 or temp == 1:
            return (x + 1) % 25
        else:
            return (x + 2) % 25

    # 时间安排
    time = 0
    for item in SectionList:  # 放入课程
        if item.credits <= 2:  # 小于2的一个课时
            count = 0
            while 1:  # 寻找合适的时间点
                newflag = 1
                for tempitem in item.busytime:  # 当前时间是否在busy段里
                    if tempitem == time:
                        newflag = 0
                        break  # 时间冲突
                if newflag == 1:  # 没有冲突· break
                    break
                time = (time + 1) % 25  # 寻找下个时间
                count = count + 1
                if count >= 25:  # 找不到时间
                    unarranged.append({'course_num': item.course.course_number, 'course_name': item.course.course.title, \
                                       'semester': item.fuck_section.semester, 'time': "unarranged", \
                                       'room': "unarranged", 'teacher_name': item.teachername,
                                       'max_num': item.capacity})
            item.timeSlot.append(time)
        elif item.credits > 2:  # 大于2的两个课时
            time = findSuitTime(time)
            count = 0
            while 1:  # 寻找合适的时间点
                newflag = 1
                for tempitem in item.busytime:
                    if tempitem == time or tempitem == time + 1:
                        newflag = 0
                        break
                if newflag == 1:
                    break
                time = findSuitTime(time + 1)
                count = count + 1
                if count >= 25:
                    unarranged.append({'course_num': item.course.course_number, 'course_name': item.course.course.title, \
                                       'semester': item.fuck_section.semester, 'time': "unarranged", \
                                       'room': "unarranged", 'teacher_name': item.teachername,
                                       'max_num': item.capacity})
            item.timeSlot.append(time)
            item.timeSlot.append(time + 1)
        time = (time + 1) % 25

    # 教室安排
    def sortClassroom(x):
        return x.capacity

    ClassroomList.sort(key=sortClassroom, reverse=True)
    judgeList = [1] * len(SectionList)  # 记录未安排的课程
    count = len(SectionList)

    for item in ClassroomList:
        if count == 0:  # 如果排完所有课
            break
        while len(item.timeSlot) != 0:  # 如果当前教室还有空
            if count == 0:  # 如果排完所有课
                break
            flag = -1
            for i in range(0, len(SectionList)):
                if judgeList[i] == 1 and SectionList[i].capacity <= item.capacity \
                        and SectionList[i].type <= item.type_equipment:  # 找到除时间外符合的教室
                    tempflag = 1
                    for j in SectionList[i].timeSlot:
                        if j not in item.timeSlot:
                            tempflag = 0
                            break
                    if tempflag == 0:  # 下一个课程
                        continue
                    flag = i
                    break
            if flag == -1:  # 当前教室没法容纳更多
                break
            judgeList[flag] = 0
            SectionList[flag].classroomID = item.classroomID
            for j in SectionList[flag].timeSlot:
                item.timeSlot.remove(j)

    if count != 0:  ##没法排完 针对剩下的多媒体课程，考虑和前面排到教室的普课交换
        for i in range(0, len(SectionList)):
            if judgeList[i] == 1 and SectionList[i].type == 2:  # 找到一个多媒体课程且没教室
                for j in range(i - 1, -1, -1):  # 找到一个普课，且时间合理
                    if SectionList[j].type == 1 and SectionList[i].busytime in SectionList[j].busytime:
                        SectionList[i].classroomID = SectionList[j].classroomID
                        judgeList[i] = 0
                        judgeList[j] = 1
    if count != 0:  # 处理普通教室
        for i in range(0, len(SectionList)):
            if judgeList[i] == 1 and SectionList[i].type == 1:  # 处理普通教室
                for item in ClassroomList:  # 企图找出合理的教室的空余时间
                    if item.capacity < SectionList[i].capacity:
                        break
                    if len(item.timeSlot):
                        if SectionList[i].credits <= 2:
                            SectionList[i].classroomID = item.classroomID
                            SectionList[i].timeSlot[0] = item.timeSlot[0]
                            item.timeSlot.remove(SectionList[i].timeSlot[0])
                            judgeList[i] = 0
                            count = count - 1
                        elif SectionList[i].credits >= 2:
                            for fuck in range(0, 5):
                                if [fuck * 5, 1 + fuck * 5] in item.timeSlot:
                                    SectionList[i].classroomID = item.classroomID
                                    SectionList[i].timeSlot = [fuck * 5, 1 + fuck * 5]
                                    item.timeSlot.remove(fuck * 5)
                                    item.timeSlot.remove(1 + fuck * 5)
                                    judgeList[i] = 0
                                    count = count - 1
                                elif [2 + fuck * 5, 3 + fuck * 5] in item.timeSlot:
                                    SectionList[i].classroomID = item.classroomID
                                    SectionList[i].timeSlot = [2 + fuck * 5, 3 + fuck * 5]
                                    item.timeSlot.remove(2 + fuck * 5)
                                    item.timeSlot.remove(3 + fuck * 5)
                                    judgeList[i] = 0
                                    count = count - 1
    if count != 0:
        for i in range(0, len(SectionList)):
            if judgeList[i] == 1:
                unarranged.append({'course_num': SectionList[i].course.course_number,
                                   'course_name': SectionList[i].course.course.title, \
                                   'semester': SectionList[i].fuck_section.semester, 'time': "unarranged", \
                                   'room': "unarranged", 'teacher_name': SectionList[i].teachername,
                                   'max_num': SectionList[i].capacity})

    # _output
    def starttime(time):
        temp = time % 5
        if temp == 0:
            return 1
        elif temp == 1:
            return 3
        elif temp == 2:
            return 6
        elif temp == 3:
            return 8
        elif temp == 4:
            return 11

    def endtime(time):
        temp = time % 5
        if temp == 0:
            return 2
        elif temp == 1:
            return 5
        elif temp == 2:
            return 7
        elif temp == 3:
            return 10
        elif temp == 4:
            return 13

    for item in SectionList:
        _day = item.timeSlot[0] / 5 + 1
        _start = starttime(item.timeSlot[0])
        if len(item.timeSlot) == 1:
            _end = endtime(item.timeSlot[0])
        else:
            _end = endtime(item.timeSlot[-1])

        findTime = TimeSlot.objects.filter(day=_day, start_time=_start, end_time=_end)
        if len(findTime) == 0:
            fuck_fuck_fuck = TimeSlot(day=_day, start_time=_start, end_time=_end)
            fuck_fuck_fuck.save()
        findTime = TimeSlot.objects.get(day=_day, start_time=_start, end_time=_end)

        forget_the_fuck = SecTimeClassroom(section=item.fuck_section, time_slot=findTime, classroom=item.classroomID)
        forget_the_fuck.save()
        ret.append({'course_num': item.courseID.course_number, 'course_name': item.courseID.title, \
                    'semester': item.fuck_section.semester, 'time': "周%d 第%d节 - 第%d节" % (_day, _start, _end), \
                    'room': "%s %s" % (item.classroomID.building, item.classroomID.room_number), \
                    'teacher_name': item.teachername, 'max_num': item.capacity})
    CourseCandiate.objects.filter().delete()
    return render(request, 'course_query_result.html', {'ret': ret, 'unarranged': unarranged})