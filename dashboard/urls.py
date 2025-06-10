from django.urls import path
from dashboard import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.LastMonth, name='dashboard-lastmonth'),
    path('lastmonth-data', csrf_exempt(views.LastMonthData), name='lastmonth-data')
]