from django.shortcuts import render
from django.http import HttpResponse,  HttpResponseRedirect
from django.contrib.auth.decorators import login_required


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
def index(request):
	user = request.user
	type = getType(user)
	if type == 'Student':
		return HttpResponseRedirect("student")
	elif type == 'Manager':
		return HttpResponseRedirect("manager")
	elif type == 'Instructor':
		return HttpResponseRedirect("instructor")
	else:
		return HttpResponse("???")

