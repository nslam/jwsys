from django.conf.urls import url

from . import views
urlpatterns=[
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login),
    url(r'^setPassword/$', views.setPassword),
    url(r'^changeInfo/$', views.changeInfo),
    url(r'^addStudent/$', views.addStudent),
    url(r'^addInstructor/$', views.addInstructor),
]