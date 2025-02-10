from django.urls import path,include
from . import views
from dashboard import views as dashboard_views


urlpatterns = [
    path('admin',views.admin_login,name='admin_login'),
    path('', views.home, name='home'),
    path('departments/', views.departments, name='departments'),
    path('doctors/', views.doctors, name='doctors'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('doctor-login/', views.doctor_login, name='doctor_login'),
    path('register/doctor/', views.doctor_register, name='doctor_register'),
    path('register/patient/', views.patient_register, name='patient_register'),
    path('patient_dashboard/<int:patient_id>/', dashboard_views.patient_dashboard, name='patient_dashboard'),
    path('doctor_dashboard/<int:doctor_id>/', dashboard_views.doctor_dashboard, name='doctor_dashboard'),
    path('admin_dashboard/', dashboard_views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', include('dashboard.urls')),
    path('delete/<str:entity_type>/<int:entity_id>/', dashboard_views.delete_entity, name='delete_entity'),
    path('__reload__/', include("django_browser_reload.urls")),
]
