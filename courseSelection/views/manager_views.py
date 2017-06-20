from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseRedirect
from .models import *
from courseSelection.dboperations.instructor_operations import *
from courseSelection.dboperations.student_operations import *
from courseSelection.dboperations.manager_operations import *
from  datetime  import  *  
import time


# Create your views here.

def show_manager(request):
	m=ManagerOperations(1)
	manager_info=m.get_manager_info()
	name = manager_info['first_name']+'-'+manager_info['last_name']
	phone_number=manager_info['phone_number']
	address=manager_info['address']
	return render(request, 'manager/index_manager.html',{'manager_name':name,'manager_phone':phone_number,'manager_addr':phone_number})

def manager_index(request):
	pass

def manager_settime_index(request):
	status='true'
	return render(request, 'manager/set_time.html', {'status': status})

def manager_set_time(request):
	start=request.POST['start_time']
	end=request.POST['end_time']
	year=request.POST['year']
	semester=request.POST['semester']
	select_round=request.POST['round']
	try:
		tran_start=datetime.strptime(start,'%Y-%m-%d %H:%M:%S')
		tran_end=datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
	except:
		status = '请按要求输入时间'
		return render(request, 'manager/set_time.html', {'status': status})

	if start!="" and end!="" and year!="":
		try:
			if tran_start<tran_end:
				m=ManagerOperations(1)
				m.set_selectionTime(tran_start,tran_end,semester,int(year),int(select_round))
				status = '设置成功'
				return render(request, 'manager/set_time.html', {'status': status})
			else:
				status = '结束时间不能早于开始时间'
				return render(request, 'manager/set_time.html', {'status': status})
		except:
			status = '设置失败，请输入正确的时间格式'
			return render(request, 'manager/set_time.html', {'status': status})
	else:
		status = '文本框不能为空'
		return render(request, 'manager/set_time.html', {'status': status})


def select_course_index(request):
	status='true'
	return render(request, 'manager/set_curriculum.html', {'status': status})

def select_course_manual(request):
	department = request.POST['department']
	major = request.POST['major']
	elective = request.POST['elective']
	public = request.POST['public']
#	return elective
	if elective!="" and public!="":
		try:
			if int(str(elective))>0 and int(str(elective))<=50 and int(str(public))>0 and int(str(public))<=50:
				try:
					m=ManagerOperations(1)
					m.set_Curriculum(department,major,elective,public)
					status = '修改成功'
					return render(request, 'manager/set_curriculum.html', {'status': status})
				except:
					status = '修改失败'
					return render(request, 'manager/set_curriculum.html', {'status': status})
			else:
				status = '请输入正确的学分'
				return render(request, 'manager/set_curriculum.html', {'status': status})
		except:
			status = '请输入合法字符'
			return render(request, 'manager/set_curriculum.html', {'status': status})
	else:
		status = '输入框不能为空'
		return render(request, 'manager/set_curriculum.html', {'status': status})


def other_setting(request):
	status='true'
	return render(request, 'manager/other_settings.html', {'status': status})


def other_setting_after(request):
	if request.method == 'POST':
		selection_limit=request.POST['selection_limit']
		drop_limit=request.POST['drop_limit']
		if selection_limit!="" and drop_limit!="":
			try:
				if int(selection_limit)>0 and int(drop_limit)>0 and int(selection_limit)<50 and int(drop_limit)<5:
					try:
						Constants.objects.filter(name='selection_limit').update(value=int(selection_limit))
						Constants.objects.filter(name='drop_limit').update(value=int(drop_limit))

						status='设置成功'
						return render(request, 'manager/other_settings.html', {'status': status})
					except:
						status='设置失败'
						return render(request, 'manager/other_settings.html', {'status': status})
				else:
					status='设置失败,请按照要求设置学分和退课数量'
					return render(request, 'manager/other_settings.html', {'status': status})
			except:
				status='设置失败,请输入合法字符'
				return render(request, 'manager/other_settings.html', {'status': status})
		else:
			status='文本框不能为空'
			return render(request, 'manager/other_settings.html', {'status': status})
	else:
		status='true'
		return render(request, 'manager/other_settings.html', {'status': status})





		



		

		