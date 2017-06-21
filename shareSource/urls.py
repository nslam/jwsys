from django.conf.urls import url
from shareSource import views
urlpatterns=[
    url(r'^$', views.mainForm),

    url(r'^homework/(?P<section_id>[0-9]+)/$', views.idjudge),
    url(r'^homework/(?P<section_id>[0-9]+)/teacher/$', views.uiforteacher),
    url(r'^homework/(?P<section_id>[0-9]+)/student/$', views.uiforstudent),
    url(r'^homework/(?P<section_id>[0-9]+)/teacher/hw/$', views.hw),

    url(r'^homework/(?P<section_id>[0-9]+)/teacher/(?P<Aid>[0-9]+)/$', views.hwforteacher),
    url(r'^homework/(?P<section_id>[0-9]+)/student/(?P<Aid>[0-9]+)/$', views.hwforstudent),
    url(r'^homework/(?P<section_id>[0-9]+)/teacher/(?P<Aid>[0-9]+)/del$', views.hwdel),
    url(r'^homework/(?P<section_id>[0-9]+)/teacher/(?P<Aid>[0-9]+)/download$', views.hwdownload),

    url(r'^sourceForm/(?P<section_id>[0-9]+)$', views.sourceForm),
    url(r'^sourceForm/(?P<section_id>[0-9]+)/del(?P<fid>[0-9]+)/$', views.filedel),
    url(r'^sourceForm/(?P<section_id>[0-9]+)/top(?P<fid>[0-9]+)/$', views.filetop),
    url(r'^sourceForm/(?P<section_id>[0-9]+)/untop(?P<fid>[0-9]+)/$', views.fileuntop),
    url(r'^sourceForm/(?P<section_id>[0-9]+)/download(?P<fid>[0-9]+)/$', views.filedownload),
]