from django.urls import path
from . import views

urlpatterns = [
    path('make-appointments/', views.make_appointments,name='make_appointments'),
    path('total-appointments/', views.make_appointments,name='total_appointments'),
    path('make_reports/<int:appointment_id>/', views.make_reports,name='make_reports'),
    path('view_reports/<int:appointment_id>', views.view_reports,name='view_reports'),
    path('my-profile/', views.profile , name ='profile'),
    path('make-appointments/', views.make_appointments , name ='make_appointments'),
    path('get_doctors/<str:department>/', views.get_doctors, name='get_doctors'),
    path('total_appointments/', views.total_appointments, name='total_appointments'),
    path('my_appointments/', views.my_appointments, name='my_appointments'),
    path('patient_list/', views.patient_list, name='patient_list'),
    path('doctor_list/', views.doctor_list, name='doctor_list'),
    path('appointment_list/', views.appointment_list, name='appointment_list'),
    path('report_list/', views.report_list, name='report_list'),
    
    ]
