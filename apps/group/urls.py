from group import views
from django.conf.urls import url


urlpatterns = [
    url(r'^/create$', views.CreateGroup),
    url(r'^/list$', views.List),
    url(r'^/GroupName$', views.GroupName),
    url(r'^/grouplist$', views.GroupList),

]
