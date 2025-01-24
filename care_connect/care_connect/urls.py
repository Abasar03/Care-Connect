"""
URL configuration for care_connect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from . import views
from dashboard import views as dashboard_views


urlpatterns = [
    path('', views.home, name='home'),
    path('departments/', views.departments, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('login/', views.login, name='login'),
    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('register/doctor/', views.doctor_register, name='doctor_register'),
    path('register/patient/', views.patient_register, name='patient_register'),
    path('patient_dashboard/<str:username>/', dashboard_views.patient_dashboard, name='patient_dashboard'),
    path('doctor_dashboard/<str:username>/', dashboard_views.doctor_dashboard, name='doctor_dashboard'),
]

