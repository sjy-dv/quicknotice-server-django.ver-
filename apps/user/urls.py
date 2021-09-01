from user import views
from django.conf.urls import url

urlpatterns = [
    url(r'^/signup$', views.SignUp),
    url(r'^/idcheck$', views.CheckId),
    url(r'^/signin$', views.SignIn),
    url(r'^/userinfo$', views.UserInfo),
    url(r'^/memberinfo$', views.MemberInfo),
]
