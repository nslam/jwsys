from django.conf.urls import url
from shareSource import views
urlpatterns=[
    url(r'^$', views.mainForm),
    #url(r'^source/(?P<section_id>[0-9]+)$', views.sourceForm),
    url(r'^homework/(?P<section_id>[0-9]+)/$', views.idjudge),
    url(r'^homework/(?P<section_id>[0-9]+)/teacher/$', views.testuiforteacher),
    url(r'^homework/(?P<section_id>[0-9]+)/student/$', views.testuiforstudent),
    url(r'^homework/(?P<section_id>[0-9]+)/teacher/hw/$',views.testhw),

    url(r'^homework/(?P<section_id>[0-9]+)/teacher/(?P<Aid>[0-9]+)/$', views.testhwforteacher),
    url(r'^homework/(?P<section_id>[0-9]+)/student/(?P<Aid>[0-9]+)/$', views.testhwforstudent),
    url(r'^homework/(?P<section_id>[0-9]+)/teacher/(?P<Aid>[0-9]+)/del$', views.testhwdel),
    url(r'^homework/(?P<section_id>[0-9]+)/teacher/(?P<Aid>[0-9]+)/download$', views.testdownload),

    url(r'^sourceForm/(?P<section_id>[0-9]+)$', views.sourceForm),
    url(r'^sourceForm/(?P<section_id>[0-9]+)/del(?P<fid>[0-9]+)/$', views.filedel),
    url(r'^sourceForm/(?P<section_id>[0-9]+)/top(?P<fid>[0-9]+)/$', views.filetop),
    url(r'^sourceForm/(?P<section_id>[0-9]+)/untop(?P<fid>[0-9]+)/$', views.fileuntop),
    url(r'^sourceForm/(?P<section_id>[0-9]+)/download(?P<fid>[0-9]+)/$', views.filedownload),
]