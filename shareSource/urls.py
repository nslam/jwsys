from django.conf.urls import url
from shareSource import views
urlpatterns=[
    url(r'^$', views.mainForm),
    url(r'^source/(?P<section_id>[0-9]+)$', views.sourceForm),
    url(r'^homework/(?P<section_id>[0-9]+)$', views.homeworkForm),
]