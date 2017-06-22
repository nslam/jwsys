from django.conf.urls import url
from . import views
urlpatterns = [
    
    url(r'^teacher1/', views.teacher1),
    url(r'^teacher3/', views.teacher3),
    url(r'^student1/', views.student1),
    url(r'^student2/', views.student2),
    url(r'^dotest/(\w+)/$', views.dotest),
    url(r'^paper1/',views.paper1),
    url(r'^paper2/(\w+)/$', views.paper2),
    url(r'^teacher1delete/(\w+)/$', views.deletepaper),
    url(r'^buildnewpaper/', views.newpaper),
    url(r'^teacher3newpd/', views.newpdquestion),
    url(r'^teacher3newxz/', views.newxzquestion),
	url(r'^teacher3delete/(\w+)/$', views.deletequestion),
	url(r'^teacher3change/(\w+)/$', views.changequestion),
	url(r'^paperchinfo/(\w+)/$', views.paperchinfo),
	url(r'paper2add/p1(\w+)p2(\w+)/$', views.paperadd),
	url(r'paper2delete/p1(\w+)p2(\w+)/$', views.paperdelete),
    url(r'teacher3search/', views.searchquestion),
    url(r'teacher2/', views.statistics),
    url(r'teacher1change/(\w+)/$', views.paperstatus),


]

