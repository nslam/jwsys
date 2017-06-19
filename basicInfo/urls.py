from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login),
    url(r'^setPassword/$', views.setPassword),
    url(r'^changeInfo/$', views.changeInfo),
    url(r'^addStudent/$', views.addStudent),
    url(r'^addInstructor/$', views.addInstructor),
    url(r'^stuGradeQuery/$', views.stuGradeQuery),
    url(r'^stuGradeAnalysis/$', views.stuGradeAnalysis),
    url(r'^addCourse/$', views.addCourse),
    url(r'^queryCourse/$', views.queryCourse),
    url(r'^gradeInput/$', views.gradeInput),
    url(r'^gradeInputDetails/$', views.gradeInputDetails),
    url(r'^gradeModify/$', views.gradeInput),
    url(r'^gradeModifyDetails/$', views.gradeInputDetails),
    url(r'^gradeQuery/$', views.gradeQuery),
    url(r'^gradeQueryDetails/$', views.gradeQueryDetails),
    url(r'^changeCourse/$', views.changeCourse),
    url(r'^dropCourse/$', views.dropCourse),
    url(r'^modifyUser/$', views.modifyUser),
    url(r'^deleteUser/$', views.deleteUser),
    url(r'^shareSource/', include('shareSource.urls')),
]
