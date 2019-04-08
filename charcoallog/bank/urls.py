from django.urls import path

from charcoallog.bank.views import HomeApi, ScheduleApi, home

app_name = 'bank'

urlpatterns = [
    path('', home, name='home'),
    path('home_api/<int:pk>/', HomeApi.as_view(), name='home_api'),
    path('schedule_api/<int:pk>/', ScheduleApi.as_view(), name='schedule_api'),
]
#   path('update/', update, name='update'),
#   path('delete/', delete, name='delete'),
