from django.shortcuts import render

def patient_dashboard(request, username):
    return render(request, 'users/patient_dashboard.html', {'username': username})

def doctor_dashboard(request, username):
    return render(request, 'users/doctor_dashboard.html', {'username': username})

def admin_dashboard(request, username):
    return render(request, 'users/admin_dashboard.html', {'username': username})
