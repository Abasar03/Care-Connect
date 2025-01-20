from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('<str:username>/doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
]




