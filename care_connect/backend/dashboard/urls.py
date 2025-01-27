from django.urls import path
from . import views

urlpatterns = [
    path('patient_dashboard/<str:username>/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor_dashboard/<str:username>/', views.doctor_dashboard, name='doctor_dashboard'),
]




