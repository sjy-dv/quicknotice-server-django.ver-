from calendars import views
from django.conf.urls import url


urlpatterns = [
    url(r'^/addcalendar$', views.CreateCalendar),
    url(r'^/list$', views.AllCalendar),
    url(r'^/detail$', views.DetailCalendar),
    url(r'^/updatecalendar$', views.UpdateCalendar),
    url(r'^/deletecalendar$', views.DeleteCalendar),
    url(r'^/alarmcard$', views.AlarmCard)
]
