from django.urls import path
from . import views

urlpatterns = [
    
    path('make-appointments/', views.make_appointments,name='make_appointments'),
    path('total-appointments/', views.make_appointments,name='total_appointments'),
    path('reports/', views.make_appointments,name='reports'),
    path('my-profile/', views.profile , name ='profile'),
    path('make-appointments/', views.make_appointments , name ='make_appointments'),
    path('get_doctors/<str:department>/', views.get_doctors, name='get_doctors'),
    path('total_appointments/', views.total_appointments, name='total_appointments'),
]
