from django.conf.urls import url, include

from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^pageClassroomInput/$', views.pageClassroomInput, name = 'pageClassroomInput'),
    url(r'^pageClassroomDelete/$', views.pageClassroomDelete, name = 'pageClassroomDelete'),
    url(r'^pageClassroomAlter/$', views.pageClassroomAlter, name = 'pageClassroomAlter'),
    url(r'^pageAutoCourseArrange/$', views.pageAutoCourseArrange, name = 'pageAutoCourseArrange'),
    url(r'^pageManuCourseArrange/$', views.pageManuCourseArrange, name = 'pageManuCourseArrange'),
    url(r'^pageInstrCourseQuery/$', views.pageInstrCourseQuery, name = 'pageInstrCourseQuery'),
    url(r'^pageClassroomCourseQuery/$', views.pageClassroomCourseQuery, name = 'pageClassroomCourseQuery'),

    url(r'^ClassroomManuInput/$', views.classroomManuInput, name = 'classroomManuInput'),
    url(r'^ClassroomFileInput/$', views.classroomFileInput, name = 'classroomFileInput'),
    url(r'^classroomDelete/$', views.classroomDelete, name = 'classroomDelete'),
    url(r'^classroomAlter/$', views.classroomAlter, name = 'classroomAlter'),
    url(r'^autoCourseArrange/$', views.autoCourseArrange, name = 'autoCourseArrange'),
    url(r'^manuCourseArrange/$', views.manuCourseArrange, name = 'manuCourseArrange'),
    url(r'^instrCourseQuery/$', views.instrCourseQuery, name = 'instrCourseQuery'),
    url(r'^classroomCourseQuery/$', views.classroomCourseQuery, name = 'classroomCourseQuery'),
    url(r'^instrBusyTimeSetting/$', views.instrBusyTimeSetting, name = 'instrBusyTimeSetting'),
    url(r'^courseInstrSetting/$', views.courseInstrSetting, name = 'courseInstrSetting'),
]