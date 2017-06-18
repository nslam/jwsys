from django.conf.urls import url

from . import views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    #url(r'^deleteUser/$', views.deleteUser),
    url(r'^look-message/$',views.lookMessage),
    url(r'^bbs-main/$',views.bbsMain),
    url(r'^send-message/$',views.sendMessage),
    url(r'^manage-notice/$', views.manageNotice),
    url(r'^manage-post/$', views.managePost),
    url(r'^post-notice/$', views.postNotice),
    url(r'^set-top/$', views.setTop),
    url(r'^set-best/$', views.setBest),
    url(r'^delete-post-manager/$', views.deletePostManager),
    url(r'^send-message-to/$', views.sendMessageTo),
    url(r'^delete-reply/$', views.deleteReply),
    url(r'^release-post/$', views.releasePost),
    url(r'^get_post=(\d+)/$', views.get_post),
    url(r'^reply/$', views.lookAndReply),
    url(r'^manage-user/$', views.manageUser),
    url(r'^search-post/$', views.search_post),
]