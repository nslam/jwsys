from django.conf.urls import url
from django.views.generic import RedirectView

from .views import student_views, instructor_views, manager_views

urlpatterns = [
	# manager
	url(r'^manager$', RedirectView.as_view(url='manager/index')),
	url(r'^manager/index$', manager_views.show_manager),
	url(r'^manager/curriculum$',manager_views.set_curriculum_demand),
	url(r'^manager/curriculum/result$',manager_views.curriculum_demand_result),
	url(r'^manager/manualselection$', manager_views.manual_selection),
	url(r'^manager/selectiontime$', manager_views.set_time),
	url(r'^manager/selectiontime/timeresult$', manager_views.time_result),
	url(r'^manager/selectiontime/confirmresult$', manager_views.confirm_result),
	url(r'^manager/setting$', manager_views.other_setting),
	url(r'^manager/setting/result$', manager_views.other_setting_result),
	url(r'^manager/manualselection$', manager_views.manual_selection),
	url(r'^manager/manualselection/result$', manager_views.selection_result),
	# instructor
	url(r'^instructor$', RedirectView.as_view(url='instructor/index')),
	url(r'^instructor/index$', instructor_views.index),
	url(r'^instructor/studentlist$', instructor_views.studentlist),
	# student
	url(r'^student$', RedirectView.as_view(url='student/index')),
	url(r'^student/index$', student_views.index),
	url(r'^student/curriculum$', student_views.curriculum),
	url(r'^student/selection$', student_views.selection),
	url(r'^student/selection/drop$', student_views.dropcourse),
	url(r'^student/selection/coursedetails$', student_views.coursedetails),
	url(r'^student/selection/priority$', student_views.selectionpriority),
	url(r'^student/selection/result$', student_views.selectionresult),
	url(r'^student/schedule$', student_views.schedule),
]
