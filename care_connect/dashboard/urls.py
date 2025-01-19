from django.urls import path,include
from . import views

urlpatterns = [
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
]
