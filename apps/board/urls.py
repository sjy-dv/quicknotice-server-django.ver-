from board import views
from django.conf.urls import urls

urlpatterns = [
    url(r'^/write$', views.Write),
    url(r'^/list$', views.BoardList),
    url(r'^/notice_list$', views.BoardNoticeList),
    url(r'^/detail$', views.BoardDetail),
    url(r'^/update$', views.BoardUpdate),
    url(r'^/delete$', views.BoardDelete),
    url(r'^/write_comment$', views.WriteComment),
    url(r'^/comment$', views.CommentList),
    url(r'^/update_comment$', views.CommentUpdate),
    url(r'^/delete_comment$', views.CommentDelete),
]
