from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseRedirect
from ..models import *
from courseSelection.dboperations.instructor_operations import *
from courseSelection.dboperations.student_operations import *
from courseSelection.dboperations.manager_operations import *
from basicInfo.models import Manager
from datetime  import  *  

from django.contrib.auth.decorators import login_required

import time
import sys


# Create your views here.

# m=ManagerOperations(1)


def getType(user):
    try:
        student = user.student
        ret = 'Student'
    except:
        try:
            instructor = user.instructor
            ret = 'Instructor'
        except:
            try:
                manager = user.manager
                ret = 'Manager'
            except:
                ret = 'none'
    return ret
    

@login_required
def show_manager(request):
	user = request.user
	type = getType(user)
	if type != 'Manager':
	    return HttpResponse('You are not a Manager!')
	manager_id = Manager.objects.get(user_id=user.id).id
	m = ManagerOperations(manager_id)

	manager_info=m.get_manager_info()
	name = manager_info['last_name'] + " " + manager_info['first_name']
	phone_number=manager_info['phone_number']
	address=manager_info['address']
	return render(request, 'manager/index.html',{'manager_name':name,'manager_phone':phone_number,'manager_addr':phone_number})


@login_required
def set_time(request):
	user = request.user
	type = getType(user)
	if type != 'Manager':
	    return HttpResponse('You are not a Manager!')
	manager_id = Manager.objects.get(user_id=user.id).id
	m = ManagerOperations(manager_id)

	return render(request, 'manager/set_time.html')


@login_required
def time_result(request):
	ctx = {}
	user = request.user
	type = getType(user)
	if type != 'Manager':
	    return HttpResponse('You are not a Manager!')
	manager_id = Manager.objects.get(user_id=user.id).id
	m = ManagerOperations(manager_id)

	try:
		start=request.GET['start_time']
		end=request.GET['end_time']
		year=request.GET['year']
		semester=request.GET['semester']
		select_round=request.GET['round']
	except:
		ctx['time_result'] = '输入不能为空！'
		return render(request, 'manager/set_time_result.html',ctx)

	if semester == 'springsummer':
		semester = 'spring&autumn'
	elif semester == 'autumnwinter':
		semester = 'autumn&winter'
	else:
		pass

	try:
		tran_start=datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
		tran_end=datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
	except:
		ctx['time_result'] = '请按要求输入时间！'
		return render(request, 'manager/set_time_result.html',ctx)

	try:
		if tran_start<tran_end:
			m.set_selection_time(tran_start,tran_end,semester,int(year),int(select_round))
			ctx['time_result'] = '设置选课时间成功！'
		else:
			ctx['time_result'] = '结束时间不能早于开始时间！'
		return render(request, 'manager/set_time_result.html',ctx)
	except:
		status = '设置失败，请输入正确的时间格式！'
		return render(request, 'manager/set_time_result.html',ctx)

	return render(request, 'manager/set_time_result.html',ctx)


@login_required
def confirm_result(request):
	user = request.user
	type = getType(user)
	if type != 'Manager':
	    return HttpResponse('You are not a Manager!')
	manager_id = Manager.objects.get(user_id=user.id).id
	m = ManagerOperations(manager_id)

	ctx = {}
	if request.GET['submit'] == 'sift':
		# year=request.GET['year']
		# semester=request.GET['semester']
		# m.decide_selection(semester, year)
		try:
			year=request.GET['year']
			semester=request.GET['semester']
			if semester == 'springsummer':
				semester = 'spring&autumn'
			elif semester == 'autumnwinter':
				semester = 'autumn&winter'
			else:
				pass
			m.decide_selection(semester, year)
			ctx['sift_result'] = '成功筛选课程！'
		except:
			ctx['sift_result'] = '筛选课程失败！'
		
		return render(request, 'manager/sift_result.html', ctx)
	if request.GET['submit'] == 'confirm':
		try:
			year=request.GET['year']
			semester=request.GET['semester']
			if semester == 'springsummer':
				semester = 'spring&autumn'
			elif semester == 'autumnwinter':
				semester = 'autumn&winter'
			else:
				pass
			m.convey_to_takes(semester, year)
			ctx['confirm_result'] = '成功确认选课！'
		except Exception as e:  
			ctx['confirm_result'] = '确认选课失败！'
		return render(request, 'manager/confirm_selection_result.html', ctx)


@login_required
def set_curriculum_demand(request):
	user = request.user
	type = getType(user)
	if type != 'Manager':
	    return HttpResponse('You are not a Manager!')
	manager_id = Manager.objects.get(user_id=user.id).id
	m = ManagerOperations(manager_id)

	ctx = {}
	# get section list
	ctx['majors'] = m.all_majors()
	return render(request, 'manager/set_curriculum.html', ctx)


@login_required
def curriculum_demand_result(request):
	user = request.user
	type = getType(user)
	if type != 'Manager':
	    return HttpResponse('You are not a Manager!')
	manager_id = Manager.objects.get(user_id=user.id).id
	m = ManagerOperations(manager_id)

	ctx = {}
	if 'major' in request.GET and 'elective_demand' in request.GET and 'public_demand' in request.GET:
		major_id = request.GET['major']
		elective_demand = request.GET['elective_demand']
		public_demand = request.GET['public_demand']
		if major_id == "" or elective_demand == "" or public_demand == "":
			ctx['result'] = '输入不能为空！'
		else:
			try:
				m.set_curriculum(int(major_id), int(elective_demand), int(public_demand))
				ctx['result'] = '设置培养方案要求成功！'
			except:
				# ctx['result'] = str(sys.exc_info()[0]) + str(sys.exc_info()[1])
				ctx['result'] = '设置培养方案要求失败！'
	else:
		ctx['result'] = '设置培养方案要求失败！'
	return render(request, 'manager/curriculum_result.html', ctx)


@login_required
def manual_selection(request):
	user = request.user
	type = getType(user)
	if type != 'Manager':
	    return HttpResponse('You are not a Manager!')
	manager_id = Manager.objects.get(user_id=user.id).id
	m = ManagerOperations(manager_id)

	ctx = {}
	if 'metric' in request.GET and 'value' in request.GET:
		ctx['sections'] = m.search_course(request.GET['metric'],request.GET['value'])
	return render(request, 'manager/help_choose.html',ctx)


@login_required
def selection_result(request):
	user = request.user
	type = getType(user)
	if type != 'Manager':
	    return HttpResponse('You are not a Manager!')
	manager_id = Manager.objects.get(user_id=user.id).id
	m = ManagerOperations(manager_id)

	ctx = {}
	if 'select' in request.POST:
		m.select_course(int(request.POST['select']),\
			int(request.POST['student_id']))
		ctx['result'] = "选课成功！"
	return render(request, 'manager/help_choose_result.html',ctx)


@login_required
def other_setting(request):
	user = request.user
	type = getType(user)
	if type != 'Manager':
	    return HttpResponse('You are not a Manager!')
	manager_id = Manager.objects.get(user_id=user.id).id
	m = ManagerOperations(manager_id)
	return render(request, 'manager/other_settings.html')


@login_required
def other_setting_result(request):
	user = request.user
	type = getType(user)
	if type != 'Manager':
	    return HttpResponse('You are not a Manager!')
	manager_id = Manager.objects.get(user_id=user.id).id
	m = ManagerOperations(manager_id)

	if request.method == 'GET':
		selection_limit=request.GET['selection_limit']
		drop_limit=request.GET['drop_limit']
		if selection_limit!="" and drop_limit!="":
			try:
				if int(selection_limit)>0 and int(drop_limit)>0 and int(selection_limit)<50 and int(drop_limit)<5:
					try:
						Constants.objects.filter(name='selection_limit').update(value=int(selection_limit))
						Constants.objects.filter(name='drop_limit').update(value=int(drop_limit))

						status='设置成功！'
						return render(request, 'manager/other_settings_result.html', {'status': status})
					except:
						status='设置失败！'
						return render(request, 'manager/other_settings_result.html', {'status': status})
				else:
					status='设置失败,请按照要求设置学分和退课数量！'
					return render(request, 'manager/other_settings_result.html', {'status': status})
			except:
				status='设置失败,请输入合法字符！'
				return render(request, 'manager/other_settings_result.html', {'status': status})
		else:
			status='输入不能为空！'
			return render(request, 'manager/other_settings_result.html', {'status': status})
	else:
		status='设置成功！'
		return render(request, 'manager/other_settings_result.html', {'status': status})





		



		

		