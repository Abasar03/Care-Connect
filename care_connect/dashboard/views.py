from django.shortcuts import render

def patient_dashboard(request):
    return render(request, 'dashboard/patient_dashboard.html')

def doctor_dashboard(request):
    return render(request, 'dashboard/doctor_dashboard.html')

def admin_dashboard(request):
    return render(request, 'dashboard/admin_dashboard.html')
