from django.conf.urls import url
from django.views.generic import RedirectView

from .views import student_views, instructor_views, manager_views

urlpatterns = [
	# manager
	url(r'^index_manager/$', manager_views.show_manager),
	url(r'^select_index/$',manager_views.select_course_index),
	url(r'^select_manager/$', manager_views.select_course_manual),
	url(r'^manager_settime_index/$', manager_views.manager_settime_index),
	url(r'^manager_set_time/$', manager_views.manager_set_time),
	url(r'^other_setting/$', manager_views.other_setting),
	url(r'^other_setting_after/$', manager_views.other_setting_after),
	# instructor
	url(r'^instructor$', RedirectView.as_view(url='instructor/index')),
	url(r'^instructor/index$', instructor_views.index),
	url(r'^instructor/studentlist$', instructor_views.studentlist),
	# student
	url(r'^student$', RedirectView.as_view(url='student/index')),
	url(r'^student/index$', student_views.index),
	url(r'^student/curriculum$', student_views.curriculum),
	url(r'^student/selection$', student_views.selection),
	url(r'^student/selection/coursedetails$', student_views.coursedetails),
	url(r'^student/selection/priority$', student_views.selectionpriority),
	url(r'^student/schedule$', student_views.schedule),
]